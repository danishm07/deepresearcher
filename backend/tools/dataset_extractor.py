import re
import requests
from bs4 import BeautifulSoup

#this script extracts data from datasets and githubs, ones that are mentioned in papers, through webscraping given urls

DATASET_KEYWORDS = [
    "dataset",
    "data set",
    "benchmark",
    "corpus",
    "collection",
]

#these are the common datasets that are used in papers, and we can use this to identify & extract them from papers
COMMON_DATASETS = [
    "imagenet", "cifar-10", "cifar-100", "mnist", "chestxray14", "mimic-iii", "squad", "pubmed",
    "commoncrawl", "wikitext", "librispeech", "coqa", "ms coco", "cityscapes", "kitti"

]

def extract_dataset_mentions(text):
    """
    Look for common dataset names and usage patterns in the text.
    """

    mentions = []
    lines = text.lower().split(". ")
    for line in lines:
        if any(keyword in line for keyword in DATASET_KEYWORDS):
            for ds in COMMON_DATASETS:
                if ds in line:
                    mentions.append({"name": ds, "context": line.strip()})
    return mentions

def extract_github_links(text):
    """
    Finding GitHub repo links in the text.
    """
    return re.findall(r"https://github.com/[^ )\n]+", text)

def build_dataset_card(mentions, github_links):
    cards = []
    for mention in mentions:
        cards.append({
            "dataset_name": mention["name"],
            "example_context": mention["context"],
            "github_repos": github_links
        })
    return cards




