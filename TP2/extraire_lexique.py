import re
import sys
import os
import argparse
import subprocess
from tabulate import tabulate
from typing import List, Dict


def convert_to_utf8(original_file, directory, original_encoding="utf-8"):
    file_path = os.path.join(directory, original_file)
    with open(file_path, "r", encoding=original_encoding, errors="ignore") as file:
        content = file.read()
    new_file = os.path.join(directory, original_file)
    with open(new_file, "w", encoding="utf-8") as file:
        file.write(content)
    return new_file


def text_list(directory):
    list_name_folder = os.listdir(directory)
    content_list = []
    for text_name in list_name_folder:
        text = ""
        text_reading_mode = open(directory + text_name, "r", encoding="UTF-8")
        text = text_reading_mode.read()
        content_list.append(text)
    return content_list


def text_list_bash(directory):
    """
    Fonction du role 1 de l'exo 3 TD2
    Prend l'argument donné sur le terminal et tranforme les contenus des fichiers en liste str
    """
    content_list = []
    for file_path in directory:
        with open(file_path, "r", encoding="UTF-8") as file:
            content_list.append(file.read())
    return content_list


def compter_frequence_mot(corpus: List[str]) -> Dict[str, int]:
    occurrences_mots = {}
    for texte in corpus:
        mots = tokeniser(texte)
        for mot in mots:
            if mot in occurrences_mots:
                occurrences_mots[mot] += 1
            else:
                occurrences_mots[mot] = 1
    return occurrences_mots


def compter_frequence_document(corpus):
    """
    Compte la fréquence de document pour chaque mot dans un corpus de documents.
    """
    compteur_documents = {}
    for texte in corpus:
        mots_uniques = set(tokeniser(texte))
        for mot in mots_uniques:
            if mot in compteur_documents:
                compteur_documents[mot] += 1
            else:
                compteur_documents[mot] = 1
    return compteur_documents


def tokeniser(text: str) -> List[str]:
    return [
        token.replace("’", "'")
        for token in re.findall(r"\b\w+?\b(?:'|’)?", text)
        if "_" not in token
    ]


def sort_dict(dic: Dict[str, int]) -> Dict[str, int]:
    return dict(sorted(dic.items(), key=lambda list: list[1], reverse=True))


def process_corpus(texts: List[str]):
    frequence_mot = sort_dict(compter_frequence_mot(texts))
    frequence_document = sort_dict(compter_frequence_document(texts))
    header = [
        "\033[1;33mMot\033[0m",
        "\033[1;34mFréquence mot\033[0m",
        "\033[1;35mFréquence document\033[0m",
    ]
    table = []
    for mot in frequence_mot:
        if frequence_mot[mot] < 20:
            break
        table.append(
            [
                f"\033[33m{mot}\033[0m",
                f"\033[34m{str(frequence_mot[mot])}\033[0m",
                f"\033[35m{str(frequence_document[mot])}\033[0m",
            ]
        )
    print(tabulate(table, header, tablefmt="fancy_grid"))


# ex3r3
def read_paths_from_stdin_and_load() -> List[str]:
    texts = []
    for line in sys.stdin:
        file_path = line.strip()
        with open(file_path, "r", encoding="UTF-8") as file:
            texts.append(file.read())
    return texts


def main():
    # dir_name = "Corpus"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--raw", help="Takes raw text from stdin.", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--from-stdin-paths",
        action="store_true",
        help="Read file paths from standard input",
    )
    parser.add_argument(
        "-f",
        "--fichiers",
        nargs="+",
        type=str,
        help="Takes filenames in argument",
    )
    args = parser.parse_args()
    if args.raw:
        # subprocess.run(["./remove_nl.sh", dir_name])
        process_corpus(sys.stdin.read().split("\n"))
    elif args.from_stdin_paths:
        texts = read_paths_from_stdin_and_load()
        process_corpus(texts)
    elif args.fichiers:
        texts = text_list_bash(args.fichiers)
        process_corpus(texts)
    else:
        print("No input method selected. Please use one of the specified methods.")
        sys.exit(1)


main()
