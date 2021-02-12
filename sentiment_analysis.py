import base64
import io
import multiprocessing as mp
import re
import string
from typing import Dict, List
from urllib import parse

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from django.conf import settings
from nltk import FreqDist, tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from plotly.offline import plot
from textblob import Sentence, TextBlob
from wordcloud import STOPWORDS, WordCloud

PROCESS_QUEUE_1: mp.Queue = mp.Queue()
PROCESS_QUEUE_2: mp.Queue = mp.Queue()
PROCESS_QUEUE_3: mp.Queue = mp.Queue()
PROCESS_QUEUE_4: mp.Queue = mp.Queue()


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        yield from tokens


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub(
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|"
            "(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            token,
        )
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = "n"
        elif tag.startswith("VB"):
            pos = "v"
        else:
            pos = "a"
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if (
            len(token) > 2
            and token not in string.punctuation
            and token.lower() not in stop_words
            and token.lower() not in STOPWORDS
        ):
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_polarity(text: str) -> float:
    return TextBlob(text).sentiment.polarity


def get_subjectivity(text: str) -> float:
    return TextBlob(text).sentiment.subjectivity


def get_analysis(polarity: int) -> str:
    if polarity < 0:
        return "negative"
    elif polarity == 0:
        return "neutral"
    else:
        return "positive"


def parse_text(text: str) -> List[Sentence]:
    return TextBlob(text).sentences


def create_dataframe(sentences: List[Sentence]) -> pd.DataFrame:
    data: Dict = {"Sentence Index": [], "Text": []}
    for index, sentence in enumerate(sentences, 1):
        data["Sentence Index"].append(index)
        data["Text"].append(str(sentence))
    df = pd.DataFrame(data=data)
    df["Polarity"] = df["Text"].apply(get_polarity)
    df["Subjectivity"] = df["Text"].apply(get_subjectivity)
    return df.sort_values(by=["Polarity"])


def create_polarity_distribution_bar_plot(df: pd.DataFrame) -> str:
    df["Analysis"] = df["Polarity"].apply(get_analysis)
    y_values = df["Analysis"].value_counts()
    fig = px.bar(
        y_values,
        y="Analysis",
        labels={"index": "Polarity", "Analysis": "Number of occurrences"},
        title="Polarity occurrences in bar graph",
    )
    data = plot(fig, output_type="div", auto_open=False)
    PROCESS_QUEUE_1.put(data)
    return data


def create_polarity_distribution_scatter_plot(df: pd.DataFrame) -> str:
    fig = px.scatter(
        df,
        x="Polarity",
        y="Subjectivity",
        title="Polarity versus Subjectivity",
    )
    data = plot(fig, output_type="div", auto_open=False)
    PROCESS_QUEUE_2.put(data)
    return data


def create_wordcloud(df: pd.DataFrame) -> str:
    all_words = " ".join(df["Text"])
    word_cloud = WordCloud(
        height=500, width=500, stopwords=STOPWORDS, collocations=False
    ).generate(all_words)
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    image = io.BytesIO()
    plt.tight_layout(pad=0)
    plt.savefig(image, format="png", facecolor="k", bbox_inches="tight")
    image.seek(0)
    string = base64.b64encode(image.read())
    data = "data:image/png;base64," + parse.quote(string)
    PROCESS_QUEUE_4.put(data)
    return data


def generate_frequency_distribution_report(df: pd.DataFrame) -> str:
    stop_words = stopwords.words("english")
    all_words = [tokenize.word_tokenize(sentence) for sentence in df["Text"]]
    cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in all_words]
    all_words = get_all_words(cleaned_tokens_list)
    data = FreqDist(all_words)
    words, counts = [], []
    for word, count in data.most_common(10):
        words.append(word)
        counts.append(count)
    fig = px.bar(
        y=counts,
        x=words,
        labels={"x": "Word", "y": "Number of occurrences"},
        title="Top 10 appearing words",
    )
    data = plot(fig, output_type="div", auto_open=False)
    PROCESS_QUEUE_3.put(data)
    return data


def generate_report(text: str) -> Dict:
    """ Using multiprocessing here gives a performance boost of ~= 2 seconds """

    sentences = TextBlob(text).sentences
    report = create_dataframe(sentences)

    if not settings.INSCRIBE_MULTIPROCESSING:
        polarity_distribution_bar_plot = create_polarity_distribution_bar_plot(report)
        polarity_distribution_scatter_plot = create_polarity_distribution_scatter_plot(
            report
        )
        frequency_distribution_report = generate_frequency_distribution_report(report)
        wordcloud = create_wordcloud(report)
    else:
        process_1 = mp.Process(
            target=create_polarity_distribution_bar_plot, args=(report,)
        )
        process_2 = mp.Process(
            target=create_polarity_distribution_scatter_plot, args=(report,)
        )
        process_3 = mp.Process(
            target=generate_frequency_distribution_report, args=(report,)
        )
        process_4 = mp.Process(target=create_wordcloud, args=(report,))
        process_1.start()
        process_2.start()
        process_3.start()
        process_4.start()
        polarity_distribution_bar_plot = PROCESS_QUEUE_1.get()
        polarity_distribution_scatter_plot = PROCESS_QUEUE_2.get()
        frequency_distribution_report = PROCESS_QUEUE_3.get()
        wordcloud = PROCESS_QUEUE_4.get()
        process_1.join()
        process_2.join()
        process_3.join()
        process_4.join()
    return {
        "report": report.to_html(
            classes=[
                "table",
                "table-dark",
                "rounded-lg",
                "table-striped",
                "table-responsive-xl",
            ],
            index=False,
            justify="center",
            show_dimensions=True,
        ),
        "polarity_distribution_bar_plot": polarity_distribution_bar_plot,
        "polarity_distribution_scatter_plot": polarity_distribution_scatter_plot,
        "wordcloud": wordcloud,
        "frequency_distribution_report": frequency_distribution_report,
    }
