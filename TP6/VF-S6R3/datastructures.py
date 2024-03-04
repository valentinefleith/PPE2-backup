from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import List
from pathlib import Path
import json


@dataclass
class Item:
    id: str
    title: str
    description: str
    categories: List[str]
    pubDate: date


@dataclass
class Corpus:
    items: list[Item]


def save_json(corpus: Corpus, output_file: Path) -> None:
    with open(output_file, "w") as file:
        json.dump(asdict(corpus), file)

def load_json(input_file: Path) -> Corpus:
    with open(input_file, "r") as file:
        data = json.load(file)
    corpus = []
    for item in data["items"]:
        corpus.append(Item(item["id"], item["title"], item["description"], item["categories"], item["pubDate"]))
    return Corpus(corpus)
