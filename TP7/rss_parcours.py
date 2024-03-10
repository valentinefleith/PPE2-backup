import re

from pathlib import Path
from typing import Optional
from datetime import date

from collections.abc import Callable

from datastructures import Item, Corpus


# on gère le filtrage des sources au niveau de l'itérateur plutôt qu'au niveau de l'article.
# cela permet d'éviter de parser un document dont on incluera aucun item de toute façon.
def iterate_pathlib(folder: str or Path, filtered_sources: Optional[list[str]]) -> list[Path]:

    """
    Renvoie une liste de fichiers candidats à la lecture.
    La liste des fichiers est filtrée selon les sources acceptées.
    """

    return sorted(
        filepath
        for filepath in Path(folder).glob("**/*.xml")
        if not filtered_sources or any(filtered_source in filepath.name for filtered_source in filtered_sources)
    )


name2iterator = {
    "glob": iterate_pathlib,
}


def filtre_categories(categories : Optional[set[str]]):
    def do_check(item: Item) -> bool:
        if not categories or not item.categories:
            return True

        return len(item.categories.intersection(categories)) != 0

    return do_check


def filtre_start_date(start_date : Optional[date]):
    def do_check(item: Item) -> bool:
        if not start_date or not item.date:
            return True

        return start_date <= item.date

    return do_check


def filtre_end_date(end_date : Optional[date]):
    def do_check(item: Item) -> bool:
        if not end_date or not item.date:
            return True

        return item.date <= end_date

    return do_check


def filtre(item: Item, filtres : list[Callable[[Item], bool]]) -> bool:
    for filtre_courant in filtres:
        if not filtre_courant(item):
            return False
    return True


# Donner des fonctions en entrée plutôt que des str évite de créer à chaque
# appel les éléments nécessaires, rendant le code plus simple ici.
# Voir: inversion of control.
def read_corpus(
    folder : str or Path,
    sources : list[str],
    iterator : Callable[[list[str or Path]], list[Path]],
    reader : Callable[[str or Path], list[Item]],
    filters : list[Callable[[Item], bool]],
) -> Corpus:

    output = {}
    
    files = iterator(folder, sources)

    for file in files:
        for item in reader(file):
            if not all(filtre(item) for filtre in filters):
                continue
            output.setdefault(item.id, item)
            output[item.id].categories.update(item.categories)

    return Corpus(list(output.values()))
