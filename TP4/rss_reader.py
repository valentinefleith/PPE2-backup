"""
Nota Bene : 
La commande à exécuter dans le terminal : python rss_reader.py -m re/et/fp <chemin_document_XML>
Ce programme permet à extraire les textes et les métadonnées des balises <item> pour n'importe quel document XML

Valentine -> Pour exec le programme :
python3 <chemin_corpus> -m re/et/fp {-fc <categories>} {-dd <date-de-debut format: YYYY-MM-DD>} {-df <date-de-fin format: YYYY-MM-DD}

"""

from pathlib import Path
import sys
import argparse
from parsing import parse_files
from filtrage import check_filtres


def load_corpus(path: str):
    current = Path(path)
    return current.rglob("*.xml")


def main():
    parser = argparse.ArgumentParser(prog="Récupérateur d'arguments")
    parser.add_argument("Path", type=str)
    parser.add_argument(
        "-m",
        "--method",
        dest="method",
        help="Choix de la methode",
        type=str,
        choices=["re", "et", "fp"],
    )
    parser.add_argument(
        "-dd", dest="date_debut", type=str, help="Date de debut : Format YYYY-MM-DD"
    )
    parser.add_argument(
        "-df", dest="date_fin", type=str, help="Date de fin : Format YYYY-MM-DD"
    )
    parser.add_argument(
        "-cat",
        "--filtre-category",
        dest="filtre_category",
        help="Pour ne selectionner qu'une seule ou plusieurs categories",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-src",
        "--filtre-source",
        dest="filtre_source",
        help="Pour ne selectionner qu'une source",
        type=str,
    )
    args = parser.parse_args()
    if not args.method:
        sys.exit("Erreur : Il faut indiquer une methode de parsing.")
    chemin = args.Path
    method = args.method
    files = load_corpus(chemin)
    parsed_corpus = parse_files(files, method)
    filtres = {
        "categories": args.filtre_category,
        "date": [args.date_debut, args.date_fin],
        "source": args.filtre_source
    }
    data = check_filtres(parsed_corpus, filtres)
    for file in data:
        for item in file:
            print(f"date : {item['pubDate']}, category : {item['category']}, source = {item['source']}")


if __name__ == "__main__":
    main()
