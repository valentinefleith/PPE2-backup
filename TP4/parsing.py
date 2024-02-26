"""
Ici les fonctions utilisées pour parser le document xml (semaine 4):
- with_re() avec le module re (r1)
- with_et() avec le module etree (r2)
- with_feedparser() avec le module feedparser (r3)
Et une fonction pour les appeler : parse_file() qui va checker la méthode
utilisée et retourner une liste. Dans cette liste, une liste par fichier ;
dans chaque sous-liste, un dictionnaire par item.
"""

import re
import xml.etree.ElementTree as ET
import feedparser
from lxml import etree


def parse_files(files, method):
    parsed_corpus = []
    for file in files:
        if method == "re":
            parsed_corpus.append(with_re(file))
        if method == "et":
            parsed_corpus.append(with_et(file))
        if method == "fp":
            parsed_corpus.append(with_feedparser(file))
    return parsed_corpus


def with_re(chemin):
    #for fichier in chemin_fichier:
    # Lecture du contenu du fichier XML
    with open(chemin, "r") as f:
        contenu = f.read()

# Expressions r√©guli√®res pour extraire les balises <item>
    item_pattern = r"<item>(.*?)</item>"
    # Recherche des correspondances dans le contenu
    items = re.finditer(item_pattern, contenu, re.DOTALL)
    donnees = []

    # It√©ration sur les correspondances des balises <item>
    for item in items:
        titre_match = re.search(r"<title>(.*?)</title>", item.group(1), re.DOTALL)
        description_match = re.search(r"<description>(.*?)</description>", item.group(1), re.DOTALL)
        categorie_match = re.findall(r"<category>(.*?)</category>", item.group(1), re.DOTALL)
        pubdate_match = re.search(r"<pubDate>(.*?)</pubDate>", item.group(1), re.DOTALL)

      #  if titre_match and description_match and categorie_match and pubdate_match:
        dictionnaire={"source":"", "title":"", "description":"", "category":[], "pubDate":""}
        dictionnaire["source"] = chemin.name
        if titre_match:
            titre = titre_match.group(1).strip()
            dictionnaire["title"] = titre
        if description_match:
            description = description_match.group(1).strip()
            dictionnaire["description"] = description
        if categorie_match:    
            categorie = categorie_match
            dictionnaire["category"] = categorie       
        if pubdate_match:
            pubdate = pubdate_match.group(1).strip()
            dictionnaire["pubDate"] = pubdate
      #  print(categorie)
            #print(dictionnaire)
            donnees.append(dictionnaire)
    return donnees

# Rôle 2 s4
def with_et(chemin):
    try:
        tree = ET.parse(chemin)
    except ET.ParseError:
        return []
    root = tree.getroot()
    id_items = root.findall(".//item")
    liste_totale = []
    title, description, pubDate = None, None, None
    for element in id_items:
        category = []
        if element.find("title") is not None:
            title = element.find("title").text
        if element.find("description") is not None:
            description = element.find("description").text
        if element.find("pubDate") is not None:
            pubDate = element.find("pubDate").text
        if element.find("category") is not None:
            for nb_category in element.findall("category"):
                category_split = nb_category.text.split(",")
                for element in category_split:
                    category.append(element)
        dictionnaire = {
            "source": chemin.name,
            "title": title,
            "description": description,
            "category": category,
            "pubDate": pubDate,
        }
        liste_totale.append(dictionnaire)

    return liste_totale


# Rôle 3 s4
def with_feedparser(chemin):
    """Prendre chemin comme argument, retourner list[dic{titre, description, date, categorie}]
    Référence : https://feedparser.readthedocs.io/en/latest/basic.html
    """
    liste_items = []
    fichier = feedparser.parse(chemin)
    items = fichier.entries
    for item in items:
        dic_data = {}
        dic_data["source"] = chemin.name
        dic_data["title"] = item.title
        if hasattr(item, "summary"):
            dic_data["description"] = item.summary
        else:
            dic_data["description"] = None
        if hasattr(item, "published"):
            dic_data["pubDate"] = item.published
        else:
            dic_data["pubDate"] = None
        if hasattr(item, "tags"):
            dic_data["category"] = item.tags[0]["term"].split(", ")
        else:
            dic_data["category"] = None
        liste_items.append(dic_data)
    return liste_items
