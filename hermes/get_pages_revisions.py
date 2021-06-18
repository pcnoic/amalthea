"""
    get_pages_revisions.py

    Grab edit revisions from a 
    WikiPedia article. Modified version
    from https://www.mediawiki.org/wiki/API:Revisions

    GNU GENERAL PUBLIC LICENSE
"""
import requests
from config import ConfigParams
import json

def get_revision_count(pagename):
    /{project}/{article}/{format}
    PROJECT = "something"
    F = "soemethig"

    

def get_page_revisions(pagename):

    S = requests.Session()
    URL = ConfigParams.WIKIPEDIA_API_URL

    REQ_PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": pagename,
        "rvprop": "timestamp|user|comment|content",
        "rvlimit": "5",
        "rvslots": "main",
        "formatversion": "2",
        "format": "json"
    }

    R = S.get(url=URL, params=REQ_PARAMS)
    DATA = R.json()

    PAGES = DATA["query"]["pages"]

    for page in PAGES:
        print(json.dumps(page["revisions"], indent=4, sort_keys=True))
