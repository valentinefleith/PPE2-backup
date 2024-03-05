'''TESTS
python3 main.py 2024 -m et -s lefigaro blast-info -c Santé -d 2023-02-01 2024-02-01
python3 main.py 2024 -m fp -s lefigaro blast-info -c Santé -d 2023-02-01 2024-02-01
python3 main.py 2024/02/06/mar.2024-02-06.21:07/Blast\ --\ articles.xml -m et -c Gaza -d 2023-02-01 2024-02-01
python3 main.py 2024 -m et -o pickle -of output.pickle
python3 main.py 2024 -m et -i pickle -if output.pickle
'''
from rss_parcours import parcourir_arborescence, filtre_categories, filtre_date, filtre_source, appliquer_filtres
from datastructures import load_pickle, save_pickle, load_json, save_json, load_xml, save_xml
import argparse

def main():
    parser = argparse.ArgumentParser(description="Programme principal : lire et filtrer des fichier RSS.")
    parser.add_argument(
        "chemin", 
        help="Chemin vers le dossier/fichier"
        )
    parser.add_argument(
        "-m",
        "--methode", 
        choices=["fp", "et"], 
        default="et", 
        help="Méthode de lecture à utiliser : 'et' etree (par défaut) | 'fp' feedparser "
        )
    # Options de filtrage
    parser.add_argument(
        "-s",
        "--source",
        nargs="+",
        help="Liste des sources à inclure (ex: -s liberation lefigaro).",
        default=['bfmtv', 'liberation', 'lefigaro', 'blast-info', 'francetvinfo', 'elucid']
        )
    parser.add_argument(
        "-c",
        "--categories", 
        nargs="+",
        help = "Catégories à filtrer (ex: -c International Politique)",
        )
    parser.add_argument(
    	"-d",
    	"--date",
    	nargs=2,
    	metavar=('DATE_DEBUT', 'DATE_FIN'),
    	help="Période de dates au format YYYY-MM-DD pour filtrer les articles (ex: -d 2024-01-01 2024-12-31)"
        )
    # Options de sauvegarde et de recharge du corpus
    parser.add_argument(
        "-i", 
        "--input",  
        choices=["pickle", "json", "xml"], 
        help="Format du fichier d'entrée (pickle, json, xml)"
        )
    parser.add_argument(
        "-o", 
        "--output",  
        choices=["pickle", "json", "xml"],  
        help="Format du fichier de sortie (pickle, json, xml)"
        )
    parser.add_argument(
        "-if", 
        "--inputfile", 
        help="Chemin du fichier d'entrée à utiliser avec --input"
        )
    parser.add_argument(
        "-of", 
        "--outputfile", 
        help="Chemin du fichier de sortie à utiliser avec --ouput"
        )

    args = parser.parse_args()

    corpus = parcourir_arborescence(args.chemin)

    if args.input:
        if args.input == "pickle":
            corpus = load_pickle(args.inputfile)
        if args.input == "json":
            corpus = load_json(args.inputfile)
        if args.input == "xml":
            corpus = load_xml(args.inputfile)

    # Liste des filtres
    filtres = []
    # Vérifier si l'option est spécifiée dans la commande 
    if args.source:
        # Si oui, ajouter le filtre à la liste de filtres
        # La fonction lambda prend un article/item en entrée et appelle la fonction filtre_source avec cet article et les sources spécifiées
        # Si l'article a la source spécifiée, le filtre retourne True, sinon False
        filtres.append(lambda item: filtre_source(item, args.source))
    if args.categories:
        filtres.append(lambda item: filtre_categories(item, args.categories))
    if args.date:
        filtres.append(lambda item: filtre_date(item, args.date[0], args.date[1]))
    # Appliquer les filtres
    articles_filtres = appliquer_filtres(corpus, filtres)

    if args.output:
        if args.output == "pickle":
            save_pickle(articles_filtres, args.outputfile)
        if args.output == "json":
            save_json(articles_filtres, args.outputfile)
        if args.output == "xml":
            save_xml(articles_filtres, args.outputfile)

    # Afficher les articles filtrés
    compt = 1
    for article in articles_filtres.items:
        print(f"n° {compt} {article}\n")
        compt += 1

if __name__ == "__main__":
    main()
