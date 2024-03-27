from tabulate import tabulate
import csv
from datastructures import Corpus, name2loader, name2saver


def verbe_nsubj(corpus: Corpus) -> dict:
    pattern = {}
    for item in corpus.items:
        for sentence in item.analysis:
            for token in sentence:
                if token.rel == "nsubj":
                    key = (token.pos, token.lemma, sentence[token.id_head - 1].lemma, sentence[token.id_head - 1].pos, token.rel)
                    if key in pattern:
                        pattern[key] += 1
                    else:
                        pattern[key] = 1
    return pattern

def comp_nom(corpus:Corpus)->dict:
    pattern = {}
    for item in corpus.items:
        for sentence in item.analysis :
            for token in sentence :
                if token.rel =="nmod":
                    key = (token.pos, token.lemma, sentence[token.id_head - 1].lemma, sentence[token.id_head - 1].pos, token.rel)
                    if key in pattern:
                        pattern[key] += 1
                    else:
                        pattern[key] = 1

    return pattern

def comp_verb(corpus: Corpus) -> dict:
    pattern = {}
    for item in corpus.items:
        for sentence in item.analysis:
            for token in sentence:
                if token.rel == "obj" and sentence[token.id_head - 1].pos == "VERB":
                    key = (token.pos, token.lemma, sentence[token.id_head - 1].lemma, sentence[token.id_head - 1].pos, token.rel)
                    verb = sentence[token.id_head - 1].lemma
                    noun = token.lemma
                    if key in pattern:
                        pattern[key] += 1
                    else:
                        pattern[key] = 1
    return pattern

def print_table(pattern: str, occ: dict):
    header = ["pattern", "lemma dep", "lemma head", "occ nb"]
    table = []
    for key, val in occ.items():
        table.append([pattern, key[0], key[1], val])
    print(tabulate(table, header, tablefmt="fancy_grid"))

def dico2csv (occ:dict, pattern:str, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Pattern','Dépendant', 'Gouverneur', 'Compte'])
        
        for key, value in occ.items():
            writer.writerow([pattern, key[0], key[1], value])

def information_mutuelle(occ:dict, pattern:str):
    header = ["predicat categorie", "lemme", "relation", "argument categorie", "lemme", "mesures frequence"]
    table = []
    for key, val in occ.items():
        table.append([key[3], key[2], key[4], key[0], key[1], val])
    print(tabulate(table, header, tablefmt="fancy_grid"))

def main(input_file, load_serialized=None, save_serialized=None, output_file=None, pattern=None):

    load_corpus = name2loader[load_serialized or "json"]

    corpus = load_corpus(input_file)
    if pattern == "vb-nsubj":
        occ = verbe_nsubj(corpus)
    elif pattern == "comp-nom":
        occ = comp_nom(corpus)
    elif pattern == "comp-vb":
        occ = comp_verb(corpus)
    

    if output_file is not None:
        dico2csv(occ, pattern, output_file)
    else:
        if pcomplex:
            print_table_complex(pattern, occ)
        else:
            information_mutuelle(occ, pattern)
            #print_table(pattern, occ)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    parser.add_argument("-s", "--save-serialized", choices = sorted(name2saver.keys()))
    parser.add_argument("-o", "--output-file", help="Output file")
    parser.add_argument("-p", "--pattern", choices=["vb-nsubj", "comp-nom", "comp-vb"]) 
    
    args = parser.parse_args()
    main(
        input_file=args.input_file,
        load_serialized=args.load_serialized,
        save_serialized=args.save_serialized,
        output_file=args.output_file,
        pattern=args.pattern
    )
