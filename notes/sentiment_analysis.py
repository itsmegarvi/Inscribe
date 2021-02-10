import re
from typing import Any, Dict, List

import pandas as pd
from textblob import Sentence, TextBlob


def remove_noise(text: str) -> str:
    """ Removes all links, @ mentions (used in twitter). """
    text = re.sub(r"https?\/\/\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    return text


def get_polarity(text: str) -> float:
    return TextBlob(text).sentiment.polarity


def parse_text(text: str) -> List[Sentence]:
    return TextBlob(text).sentences


def create_dataframe(sentences: List[Sentence]) -> Any:
    data: Dict = {"Sentence Token": [], "Text": [], "Polarity": []}
    for index, sentence in enumerate(sentences, 1):
        data["Sentence Token"].append(index)
        data["Text"].append(str(sentence))
        data["Polarity"].append(sentence.polarity)
    return pd.DataFrame(data=data).sort_values(by=["Polarity"])


def generate_report(text: str) -> Dict:
    sentences = TextBlob(text).sentences
    report = create_dataframe(sentences)
    # report.reset_index(drop=True, inplace=True)
    return {
        "report": report.to_html(
            classes=["table", "table-dark", "rounded-lg", "table-striped"],
            index=False,
            justify="center",
            show_dimensions=True,
        )
    }
