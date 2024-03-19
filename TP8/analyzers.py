from datastructures import Token, Item, name2loader, name2saver


def load_spacy():
    import spacy
    return spacy.load("fr_core_news_sm")


def load_stanza():
    import stanza
    #stanza.download("fr")  # téléchargé qu'une fois, peut se commenter
    return stanza.Pipeline("fr", processors="tokenize,pos,lemma,depparse")


def load_trankit():
    import trankit
    return trankit.Pipeline('french', gpu=False)


def analyze_spacy(parser, article: Item) -> Item:
    result = parser((article.title or "") + "\n" + (article.description or ""))
    sentences = []
    for sent in result.sents:
        tokens = []
        for token in sent:
            if token.text.strip():
                tokens.append(Token(token.text, token.lemma_, token.pos_, token.head.i, token.dep_))
        sentences.append(tokens)
    article.analysis = sentences
    print("\nAnalysis for article: ", article.title)
    for sentence in sentences:
        print(sentence)
    return article


def analyze_stanza(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sent in result.sentences:
        sentences = []
        for token in sent.words:
            sentences.append(Token(token.text, token.lemma, token.upos, token.head, token.deprel))
        output.append(sentences)
    article.analysis = output
    return article


def analyze_trankit(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sentence in result['sentences']:
        sentences = []
        for token in sentence['tokens']:
            if 'expanded' not in token.keys():
                token['expanded'] = [token]
            for w in token['expanded']:
                sentences.append(Token(w['text'], w['lemma'], w['upos'],w['head'], w['deprel']))
            output.append(sentences)
    article.analysis = output
    return article



name2analyzer = {
    "spacy": (load_spacy, analyze_spacy),
    "stanza": (load_stanza, analyze_stanza),
    "trankit": (load_trankit, analyze_trankit),
}


def main(input_file, load_serialized=None, save_serialized=None, output_file=None, analyzer=None):
    DEMO_HARD_LIMIT = 10 # pour faire une démonstration au besoin

    load_corpus = name2loader[load_serialized or "json"]
    save_corpus = name2saver[save_serialized or "json"]
    load_model, analyze = name2analyzer[analyzer]

    corpus = load_corpus(input_file)
    model = load_model()
    
    #corpus.items = corpus.items[:DEMO_HARD_LIMIT]  # commenter pour traiter tout le corpus
    corpus.items = [analyze(model, item) for item in corpus.items]

    if output_file:
        save_corpus(corpus, output_file)
    else :
        print(corpus)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    parser.add_argument("-s", "--save-serialized", choices = sorted(name2saver.keys()))
    parser.add_argument("-o", "--output-file", help="Output file")
    parser.add_argument("-a", "--analyzer", choices=sorted(name2analyzer.keys()))
    
    args = parser.parse_args()
    main(
        input_file=args.input_file,
        load_serialized=args.load_serialized,
        save_serialized=args.save_serialized,
        output_file=args.output_file,
        analyzer=args.analyzer
    )
