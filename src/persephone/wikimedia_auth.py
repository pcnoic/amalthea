"""
    OAuth owner-only consumers authenticating against WikiPedia's API
"""

import requests
from config import ConfigParams


class WikimediaAuth:

    """
        Fetches an API action token.
        Most common token type: login
        See more: https://www.mediawiki.org/wiki/API:Tokens
    """
    def get_API_token():
        S = requests.session()
        URL = ConfigParams.WIKIPEDIA_API_URL

        PARAMS = {
            "action":"query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        req = S.get(url=URL, params=PARAMS)
        res = req.json()

        return res["query"]["tokens"]["logintoken"]

    """
        Sending post request to login.
        Requires API:Token of type 'login'
    """
    def get_login(token):
        S = requests.Session()
        URL = ConfigParams.WIKIPEDIA_API_URL

        PARAMS = {
            "action":"login",
            "lgname":"your_bot_username",
            "lgpassword":"your_bot_password",
            "lgtoken":token,
            "format":"json"
        }

        req = S.post(URL, data=PARAMS)
        res = req.json()

        print(res)

    """
        Identity Verifier
    """
    def verify_wikiId(username):
        print(username)
