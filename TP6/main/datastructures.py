from dataclasses import dataclass, asdict
from typing import List
import pickle
from pathlib import Path
import json
import xml.etree.ElementTree as ET

@dataclass
class Item:
    titre: str
    description: str
    date: str
    categories: List[str]
    source: str

@dataclass
class Corpus:
    items: List[Item]

def save_pickle(corpus: Corpus, output_file: str) -> None:
    with open(output_file, 'wb') as file:
        pickle.dump(corpus, file, pickle.HIGHEST_PROTOCOL)

def load_pickle(input_file: str) -> Corpus:
    with open(input_file, 'rb') as file:
        corpus = pickle.load(file)
    return corpus

def save_json(corpus: Corpus, output_file: Path) -> None:
    with open(output_file, "w") as file:
        json.dump(asdict(corpus), file)

def load_json(input_file: Path) -> Corpus:
    with open(input_file, "r") as file:
        data = json.load(file)
    corpus = []
    for item in data["items"]:
        corpus.append(Item(item["titre"], item["description"], item["date"], item["categories"], item["source"]))
    return Corpus(corpus)

def save_xml(corpus:Corpus, output_file:Path) -> None:
    fichier_corpus = Path(output_file)
    if fichier_corpus.suffix != ".xml":
        output_file = input("Veuillez entrer un chemin d'un fichier XML \n")
        save_xml(corpus, output_file)
    else:
        root = ET.Element("root")
        for i in corpus.items:
            
            item = ET.Element("item")
            root.append(item)

            for cat in range(len(i.categories)):
                category = ET.Element("category")
                category.text = i.categories[cat]
                item.append(category)
            
            title = ET.Element("title")
            title.text = i.titre
            item.append(title)

            description = ET.Element("description")
            description.text = i.description
            item.append(description)

            pubDate = ET.Element("pubDate")
            pubDate.text = i.date
            item.append(pubDate)

            source = ET.Element("source")
            source.text = i.source
            item.append(source)

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
    return None

def load_xml(input_file:Path) -> Corpus:
    if Path(input_file).suffix != ".xml":
        input_file = input("Veuillez entrez un fichier xml. \n")
        return load_xml(input_file)
    else:
        tree = ET.parse(input_file)
        root = tree.getroot()
        list_items = []
        for item in root.findall(".//item"):
            datas = Item("", "", "", [], "")
            for child in item:
                if child.tag == "category":
                    datas.categories.append(child.text)

                elif child.tag == "title":
                    datas.titre = child.text

                elif child.tag == "description":
                    datas.description = child.text

                elif child.tag == "pubDate":
                    datas.date = child.text
                
                elif child.tag == "source":
                    datas.source = child.text

            list_items.append(datas)
        corpus = Corpus(list_items)

    return corpus