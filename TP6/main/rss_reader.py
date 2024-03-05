import argparse
from pathlib import Path
from datastructures import Item
from typing import List
import feedparser
import xml.etree.ElementTree as ET

def lire_fichier(path, method="et"):
    try:
        if method == "et":
            return lire_fichier_etree(path)
        elif method == "fd":
            return lire_fichier_feedparser(path)
        else:
            raise ValueError("Méthode de lecture non prise en charge : veuillez spécifier 'et' pour etree ou 'fp' pour feedparser.")

    except Exception as e:
        print(f"Erreur : {e}")
        pass

used_links=[]

def lire_fichier_etree(filename: str) -> List[Item]:
    global used_links 
    articles = []
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        for elem in root.iter("item"):
            lien = elem.find("link").text if elem.find("link") is not None else None
            # Vérifier si le lien de l'article est déjà présent dans les liens déjà utilisés
            if lien in used_links:
                continue
            used_links.append(lien)
            
            titre = elem.find("title").text if elem.find("title") is not None else None
            date = elem.find("pubDate").text if elem.find("pubDate") is not None else None
            categories = [category.text for category in elem.findall("category")]
            description = elem.find("description").text if elem.find("description") is not None else None
            source = (lien.split('//')[-1].split('/')[0].replace('www.', '').split('.')[0]) if lien is not None else None

            # Création d'une instance de la classe Item
            article = Item(titre, description, date, categories, source)
            articles.append(article)
    except ET.ParseError:
        pass
    return articles


def lire_fichier_feedparser(filename: str) -> List[Item]:
    global used_links 
    articles = []
    
    try:
        feed = feedparser.parse(filename)
        
        for entry in feed.entries:
            lien = entry.link if 'link' in entry else None
            # Vérifier si le lien de l'article est déjà présent dans les liens déjà utilisés
            if lien in used_links:
                continue
            used_links.append(lien) 
            
            titre = entry.title if 'title' in entry else None
            date = entry.published if 'published' in entry else None
            categories = [category.term for category in entry.tags] if 'tags' in entry else []
            description = entry.summary if 'summary' in entry else None
            source = (lien.split('//')[-1].split('/')[0].replace('www.', '').split('.')[0]) if lien is not None else None
            
            # Création d'une instance de la classe Item
            article = Item(titre, description, date, categories, source)
            articles.append(article)
    except Exception as e:
        print(f"Erreur: {e}")
    return articles

def main():
    parser = argparse.ArgumentParser(description="Lire un fichier RSS et afficher son contenu.")
    parser.add_argument(
        "chemin", 
        help="Chemin vers le fichier XML"
        )
    parser.add_argument(
        "-m",
        "--methode", 
        choices=["fd", "et"], 
        default="et", 
        help="Méthode de lecture à utiliser : 'et' etree (par défaut) | 'fp' pour feedparser"
        )
    args = parser.parse_args()

    items = lire_fichier(args.chemin, method=args.methode)
    for item in items:
        print(item, "\n")

if __name__ == "__main__":
    main()