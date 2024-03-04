import re

from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Optional
from datetime import datetime, date
from dateutil import parser as dateparser
import feedparser

from datastructures import Item


def rss_reader_etree(filename: str | Path) -> list[dict]:
    name = Path(filename).name
    if name.lower() in ("flux.xml", "flux rss.xml"):  # erreur de parsing
        return []

    root = ET.parse(filename)

    output = []
    global_categories = set()

    for cat_tag in root.iterfind("category"):
        global_categories.add(cat_tag.text)

    for item in root.iterfind(".//item"):
        dataid = item.find("guid").text

        title = item.find("title")
        if title is not None:
            title = title.text

        description = item.find("description")
        if description is not None:
            description = description.text

        pubdate = item.find("pubDate")
        if pubdate is None:
            pubdate = item.find("lastpublished")
        else:
            pubdate = pubdate.text
        
        categories = [category.text for category in item.findall("category")]
        # categories = global_categories.copy()
        # for cat_tag in item.iterfind("category"):
        #     categories.add(cat_tag.text)
        article = Item(dataid, title, description, categories, pubdate)
        # article = {
        #     "id": dataid,
        #     "title": title,
        #     "description": description,
        #     "date": pubdate,
        #     "categories": categories,
        # }
        output.append(article)

    return output


def rss_reader_feedparser(filename: str | Path) -> list[dict]:
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
            item.id, item.title, item.get("description"), categories, pubdate
        )
        # article = {
        #     "id": item.id,
        #     "title": item.title,
        #     "description": item.get("description"),
        #     "date": pubdate,
        #     "categories": categories,
        # }
        output.append(article)

    return output
