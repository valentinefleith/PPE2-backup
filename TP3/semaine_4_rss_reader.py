import argparse
from sys import exit
from typing import List, Dict
from lxml import etree
import feedparser


def main():
    arguments = parser()
    if not arguments.read_method:
        print("Le script a besoin que vous choissiez une option -r entre 're', 'et', et 'fp'")
        exit()
    if arguments.read_method == "re":
        extraction_regex(arguments.argument)
    elif arguments.read_method == "et":
        extraction_etree(arguments.argument)
    elif arguments.read_method == "fp":
        extraction_feedparser(arguments.argument)


def parser():
    parsing = argparse.ArgumentParser(
        prog="ExtractionData",
        description="Extrait les donnees textuelles (titres et descriptions) et les metadonnees (categories et date de publication) de fichiers xml"
        )
    parsing.add_argument("argument", help="la fonction prend en argument un fichier xml")
    parsing.add_argument(
        "-r",
        "--read-method",
        choices=["re", "et", "fp"],
        help="l'option 're' utilise des regex, l'option 'et' utilise etree et l'option 'fp' utilise feedparser"
        )
    arguments = parsing.parse_args()
    return arguments


def extraction_regex(path):
    import re

    with open(f"{path}", "r", encoding="utf-8") as file:
        texte = file.read()
        items = re.findall(r"<item>.*?</item>", texte, re.DOTALL)
        data_liste = ["title", "description", "category", "pubDate"]
        
        liste_complete = [
            {data_type: re.search(fr"<{data_type}>(.*)</{data_type}>", item, re.DOTALL).group(1)
             for data_type in data_liste
            }
            for item in items]

    print(liste_complete)
    return liste_complete


def extraction_etree(file: str) -> List[Dict[str, str]]:
    tree = etree.parse(file)
    items = tree.xpath("//item")
    data = ["title", "description", "category", "pubDate"]
    items_data = [
        {
            child.tag: child.text.strip()
            for child in item.getchildren()
            if child.tag in data
        }
        for item in items
    ]
    print(items_data)
    return items_data


def extraction_feedparser(corpus):
    d = feedparser.parse(corpus)
    e = d.entries[0:]  # Je le fais pour que feedparser puisse extraire tous les items
    liste = []
    for entry in e:
        dictionnaire = {
            "title": entry.title,
            "description": entry.description,
            "pubDate": entry.published,
            "category": entry.category
        }
        liste.append(dictionnaire)
   
    print(liste)
    return liste

   
if __name__ == '__main__':
    main()
