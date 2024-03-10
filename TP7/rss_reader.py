import re

from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Optional
from dateutil import parser as dateparser

import feedparser

from datastructures import Item


def rss_reader_etree(filename: str or Path) -> list[Item]:
    name = Path(filename).name
    if name.lower() in ("flux.xml", "flux rss.xml"): # erreur de parsing
        return []

    root = ET.parse(filename)

    output = []
    global_categories = set()

    for cat_tag in root.find("channel").iterfind("category"):
        global_categories.add(cat_tag.text)

    for item in root.iterfind(".//item"):
        dataid = item.find("guid").text

        # particularité etree : ne pas vérifier la valeur avec juste if, mais bien avec "is None" ou "is not None"
        # doc : https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element.remove
        title = item.find("title")
        if title is not None:
            title = title.text

        description = item.find("description")
        if description is not None:
            description = description.text

        pubdate = item.find("pubDate")
        if pubdate is None:
            pubdate = item.find("lastpublished")
        if pubdate is not None:
            pubdate = dateparser.parse(pubdate.text)
        else:
            pubdate = None

        categories = global_categories.copy()
        for cat_tag in item.iterfind("category"):
            categories.add(cat_tag.text)

        article = Item(
            id=dataid,
            source=name,
            title=title,
            description=description,
            date=pubdate,
            categories=categories,
        )
        output.append(article)

    return output


def rss_reader_feedparser(filename: str or Path) -> list[Item]:
    feed = feedparser.parse(filename)
    output = []
    global_categories = set(t["term"] for t in feed.feed.get("tags", []))

    for item in feed["entries"]:
        pubdate = item.get("published")
        if not pubdate:
            pubdate = item.get("lastpublicationdate")
        if pubdate:
            pubdate = dateparser.parse(pubdate)

        categories = global_categories.copy()
        categories.update(t["term"] for t in item.get("tags", []))

        article = Item(
            id=item.id,
            source=filename.name,
            title=item.title,
            description=item.get("description"),
            date=pubdate,
            categories=categories,
        )
        output.append(article)

    return output


name2reader = {
    "etree":      rss_reader_etree,
    "feedparser": rss_reader_feedparser,
}
