from datetime import datetime, date
from pathlib import Path
from rss_reader import rss_reader_etree, rss_reader_feedparser
from rss_parcours import iterate_pathlib, filtre
from datastructures import Item, Corpus, save_json, load_json

name2reader = {
    "etree": rss_reader_etree,
    "feedparser": rss_reader_feedparser,
}

name2iterator = {
    "glob": iterate_pathlib,
}

name2saver = {
    # "pickle": save_pickle,
    "json": save_json,
    # "xml": save_xml,
}

name2loader = {
    # "pickle": save_pickle,
    "json": load_json,
    # "xml": save_xml,
}


def main(
    filename,
    rss_reader=None,
    iterator=None,
    loader=None,
    saver=None,
    input_file=None,
    output_file=None,
    start_date=None,
    end_date=None,
    categories=None,
    sources=None,
):
    reader = name2reader[rss_reader or "feedparser"]
    iterator = name2iterator[iterator or "glob"]
    saver = name2saver[saver or "json"]
    if loader is not None:
        loader = name2loader[loader]
        corpus = loader(input_file)
        print(corpus)
        return

    start_date = start_date and datetime.fromisoformat(start_date)
    categories = set(categories or [])
    sources = sources or []

    # TODO: attention, ce code ne fait pas de déduplication !
    output: list[Item] = []
    for filepath in iterator(filename):
        if not sources or any(src in str(filepath) for src in sources):
            articles = [
                art
                for art in reader(filepath)
                if filtre(art, start_date=start_date, categories=categories)
            ]
            output.extend(articles.copy())
    output = Corpus(output)
    if output_file is None:
        output_file = "output.json"
    saver(output, output_file)
    print(len(output.items))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-r", "--rss-reader", choices=sorted(name2reader.keys()))
    parser.add_argument("-i", "--iterator", choices=sorted(name2iterator.keys()))
    parser.add_argument("-s", "--start-date", help="date in ISO format YYYY-MM-DD")
    parser.add_argument("-e", "--end-date", help="date in ISO format YYYY-MM-DD")
    parser.add_argument(
        "-c",
        "--categories",
        nargs="*",
        help="liste des catégories à considérer (article OK = une parmi la liste)",
    )
    parser.add_argument(
        "--sources",
        nargs="*",
        help="liste des sources à considérer (article OK = une parmi la liste)",
    )
    parser.add_argument("--load", choices=sorted(name2loader.keys()))
    parser.add_argument("-if", "--input_file", help="fichier a partir duquel recuperer le corpus")
    parser.add_argument("--save", choices=sorted(name2saver.keys()))
    parser.add_argument("-of" ,"--output_file", help="fichier dans lequel enregistrer le corpus")

    args = parser.parse_args()
    main(
        args.filename,
        args.rss_reader,
        args.iterator,
        loader=args.load,
        saver=args.save,
        input_file=args.input_file,
        output_file=args.output_file,
        start_date=args.start_date,
        end_date=args.end_date,
        categories=args.categories,
        sources=args.sources,
    )
