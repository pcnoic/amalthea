"""
    get_pages_revisions.py

    Grab edit revisions from a 
    WikiPedia article. Modified version
    from https://www.mediawiki.org/wiki/API:Revisions

    GNU GENERAL PUBLIC LICENSE
"""
from re import X
from fastapi_users import user
import requests
from requests.exceptions import URLRequired
from config import ConfigParams
import json

class Revisions:


    def search_wiki(searchterm):
        S = requests.Session()
        REQ_PARAMS = {
            "action":"query",
            "format":"json",
            "list":"search",
            "srsearch": searchterm
        }
        
        req = S.get(url=ConfigParams.WIKIPEDIA_API_URL, params=REQ_PARAMS)
        res = req.json()
        
        RESULTS = res["query"]["search"]
        
        
        return {"results": RESULTS}

    def get_own_revisions(username, pageid):

        S = requests.Session()
        
        # Fetch Title from pageid
        PAGE_REQ_PARAMS = {
            "action": "query",
            "pageids": pageid,
            "format": "json",
            "formatversion": 2
        }
        
        page_req = S.get(url=ConfigParams.WIKIPEDIA_API_URL, params=PAGE_REQ_PARAMS)
        page_res = page_req.json()
        
        PAGE = page_res["query"]["pages"]
        PAGE_TITLE = PAGE[0]["title"]
        print(PAGE_TITLE)
        
        # Fetch revisions of page, return only those that were written by username
        REV_REQ_PARAMS = {
            "action": "query",
            "prop": "revisions",
            "titles": PAGE_TITLE,
            "rvprop": "timestamp|user|ids",
            "rvlimit": ConfigParams.MAX_WIKIPEDIA_REV,
            "rvslots": "main",
            "formatversion": "2",
            "format": "json"
        }

        rev_req = S.get(url=ConfigParams.WIKIPEDIA_API_URL, params=REV_REQ_PARAMS)
        rev_res = rev_req.json()

        PAGE = rev_res["query"]["pages"]
        REVISIONS = []
        USER_REVISIONS = []
        
        for key in PAGE:
            REVISIONS = key["revisions"]
            for revision in REVISIONS:
                if revision["user"] == username:
                    USER_REVISIONS.append(revision)
            

        return {"results":USER_REVISIONS}

    def get_revision_content(revid):
        S = requests.Session()
        
        # Fetch content of revision
        REQ_PARAMS = {
            "action":"query",
            "prop":"revisions",
            "rvprop":"content",
            "format":"json",
            "formatrevision":"2",
            "revids":revid
        }
        
        req = S.get(url=ConfigParams.WIKIPEDIA_API_URL, params=REQ_PARAMS)
        res = req.json()
        
         
        
        print(res)
        