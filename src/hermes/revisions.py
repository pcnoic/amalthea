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

class Revisions:

    def get_revision_count(pagename):
        PROJECT = "something"
        F = ""


    def get_own_revisions(article_id):

        S = requests.Session()
        URL = ConfigParams.WIKIPEDIA_API_URL

        REQ_PARAMS = {
            "action": "query",
            "prop": "revisions",
            "titles": article_id,
            "rvprop": "timestamp|user|comment|content",
            "rvlimit": ConfigParams.MAX_WIKIPEDIA_REV,
            "rvslots": "main",
            "formatversion": "2",
            "format": "json"
        }

        req = S.get(url=URL, params=REQ_PARAMS)
        res = req.json()

        PAGES = res["query"]["pages"]

        for page in PAGES:
            print(json.dumps(page["revisions"], indent=4, sort_keys=True))
