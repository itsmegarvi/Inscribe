import re
from typing import Any, Dict, List

import pandas as pd
from django.db.models import Model
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
    data: Dict = {"index": [], "text": [], "polarity": []}
    for index, sentence in enumerate(sentences, 1):
        data["index"].append(index)
        data["text"].append(str(sentence))
        data["polarity"].append(sentence.polarity)
    return pd.DataFrame(data=data)


def generate_report(text: str) -> Dict:
    sentences = TextBlob(text).sentences
    report = create_dataframe(sentences)
    return {"report": report}


# test = create_dataframe(
#     parse_text(
#         "hello I am under the water. 10 minutes more! Hello bro, I feel so awesome..."
#     )
# )
# print(test)
