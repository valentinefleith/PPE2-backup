from pathlib import Path
from datastructures import Corpus, Item
from typing import List, Callable
from rss_reader import lire_fichier

def iterate_pathlib(folder: str) -> list[Path]:
    folder_path = Path(folder)
    if folder_path.is_dir():
        return sorted(folder_path.glob("**/*.xml"))
    elif folder_path.is_file() and folder_path.suffix.lower() == '.xml':
        return [folder_path]
    else:
        print("Le chemin spécifié n'est ni un répertoire ni un fichier XML.")
        return []

def parcourir_arborescence(path: str) -> Corpus:
    corpus = Corpus(items=[])

    for file_path in iterate_pathlib(path):
        items = lire_fichier(file_path)
        corpus.items.extend(items)

    return corpus

def filtre_date(item: Item, date_debut: str, date_fin: str) -> bool:
    from datetime import datetime
    from dateutil import parser
    try:
        # Conversion des dates de début et de fin données en args en objets datetime
        debut_date = datetime.strptime(date_debut, '%Y-%m-%d')
        fin_date = datetime.strptime(date_fin, '%Y-%m-%d')
        # Récupération de la date de l'article
        date = item.date
        if date:
            # Conversion de la date de l'article en objet datetime
            conv_date = parser.parse(date).replace(tzinfo=None)
            # Vérification de si la date de l'article est dans la période spécifiée
            return debut_date <= conv_date <= fin_date
    except ValueError:
        print(f"La date de l'article {item.date} n'est pas dans un format valide.")
    return False

def filtre_source(item: Item, sources_acceptees: List[str]) -> bool:
    return item.source in sources_acceptees

def filtre_categories(item: Item, categories_acceptees: List[str]) -> bool:
    return any(category in categories_acceptees for category in item.categories)

def appliquer_filtres(corpus: Corpus, filtres: List[Callable[[Item], bool]]) -> Corpus: # List[Callable[[Item], bool]] est la liste des fonctions de filtrage
    corpus_filtre = Corpus(items=[])
    articles_filtres = [] # Liste qui contiendra les articles qui passent tous les filtres
    for article in corpus.items: # Itèrer sur chaque article/Item du corpus 
        # Appliquer chaque fonction de filtrage à l'article en cours de traitement, all() renvoie True si toutes les fonctions de filtrage return True pour cet article
        if all(filtre(article) for filtre in filtres): 
            articles_filtres.append(article)
    corpus_filtre.items.extend(articles_filtres)
    return corpus_filtre
