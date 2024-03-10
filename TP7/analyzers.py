#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
usage: analysers [-h] [-l {json,pickle,xml}] [-t {spacy,stanza,trankit}] [-z {json,pickle,xml}] input_file output_file
ex : python3 analysers.py -l json -t trankit -z json mon_corpus.json mon_corpus_enchichi.json
"""

import argparse
from pathlib import Path

import spacy
import stanza
from trankit import Pipeline

from datastructures import Item, Token, name2loader, name2saver


def parser():
    parsing = argparse.ArgumentParser(
        prog="analysers",
        description = "enrichit un fichier Corpus d'Items (text, lemme et upos)")
    parsing.add_argument("input_file", help="fichier d'entree")
    parsing.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()),
        help = "format du fichier d'entree")
    parsing.add_argument("-t", "--tool", choices = sorted(name2library.keys()),
        help = "outil d'analyse du texte: spacy, stanza ou trankit")
    parsing.add_argument("-z", "--save-serialized", choices = sorted(name2saver.keys()),
        help = "format du fichier de sortie")
    parsing.add_argument("output_file", help = "fichier de sortie")

    args = parsing.parse_args()
    return args


###################SPACY#######################################
def analyse_spacy(item: Item) -> Item:
    nlp = spacy.load("fr_core_news_sm")
    item.tokens = tag_with_spacy(nlp, item.title, item.description)
    return item


def tag_with_spacy(nlp, title, description) -> list[Token]:
    title, description = nlp(title), nlp(description)
    title_tags = [
        Token(token.text, token.pos_, token.lemma_) for token in title
    ]
    description_tags = [
        Token(token.text, token.pos_, token.lemma_) for token in description
    ]
    title_tags.extend(description_tags)
    return title_tags


#####################STANZA#####################################
def analyse_stanza(item: Item) -> Item:
    nlp = stanza.Pipeline("fr", processors="tokenize, pos, lemma")
    item.tokens = tag_with_stanza(nlp, item.title, item.description)
    return item


def tag_with_stanza(nlp: stanza.Pipeline, title: str, description: str) -> list[Token]:
    doc_title, doc_description = nlp(title), nlp(description)
    title_tags = [
        Token(text=token.text, pos=token.pos, lemma=token.lemma) for sent in doc_title.sentences for token in sent.words
    ]
    description_tags = [
        Token(text=token.text, pos=token.pos, lemma=token.lemma) for sent in doc_description.sentences for token in
        sent.words
    ]
    title_tags.extend(description_tags)
    return title_tags


###################TRANKIT#######################################
def analyse_trankit(item: Item)-> Item:
    p = Pipeline('french')
    titre = item.title
    description = item.description
    
    for element in [titre, description]:
        processed_text = p(element)
        for sentence in processed_text["sentences"]:
            for token in sentence["tokens"]:
                if item.tokens is None:
                    item.tokens = []
                    
                item.tokens.append(Token(
                    token["text"],
                    token["lemma"],
                    token["upos"]
                    ))
    
    return item


name2library = {
    "spacy": analyse_spacy,
    "stanza": analyse_stanza,
#    "trankit": analyse_trankit
}    


def main():
    args=parser()
    
    if args.load_serialized:
        loader = name2loader[args.load_serialized]
        corpus = loader(Path(args.input_file))
        
    if args.tool:
        library= name2library[args.tool]
        for item in corpus.items: 
            item = library(item)
                
    if args.save_serialized and args.output_file:
        saver = name2saver[args.save_serialized]
        saver(corpus, Path(args.output_file))

    
    print(f"Exemple d'item :\n{corpus.items[0]}")


if __name__ == "__main__":
    main()
