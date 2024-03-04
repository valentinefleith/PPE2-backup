from pathlib import Path
from typing import Optional
from datetime import datetime, date
from dateutil import parser as dateparser

from datastructures import Item


def iterate_pathlib(folder: str | Path) -> list:
    return sorted(Path(folder).glob("**/*.xml"))


name2iterator = {
    "glob": iterate_pathlib,
}


def filtre_categories(item: Item, categories: Optional[set[str]]):
    if not categories:
        return True

    item_categories = item.categories

    if not item_categories:
        return True  # return False possible

    return len(item_categories.intersection(categories)) != 0


def filtre_start_date(item: Item, start_date: Optional[date]):
    if not start_date:
        return True

    pubdate = item.pubDate

    if pubdate is None:
        return True  # return False possible

    return start_date <= pubdate


# TODO: pensez à ajouter le reste des filtres !
# ou mieux, voir pour python: currying, closures
def filtre(item: Item, start_date: Optional[date], categories: Optional[set] = None):
    if not filtre_categories(item, categories):
        return False
    if not filtre_start_date(item, start_date):
        return False
    return True
