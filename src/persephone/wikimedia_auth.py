"""
    OAuth owner-only consumers authenticating against WikiPedia's API
"""

from fastapi_users import user
import requests
from config import ConfigParams


class WikimediaAuth:

    """
        Fetches an API action token.
        Most common token type: login
        See more: https://www.mediawiki.org/wiki/API:Tokens
    """
    def get_API_token(self):
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
    def get_login(self, username, password, token):
        S = requests.Session()
        URL = ConfigParams.WIKIPEDIA_API_URL

        PARAMS = {
            "action":"login",
            "lgname":username,
            "lgpassword": password,
            "lgtoken":token,
            "format":"json"
        }

        req = S.post(URL, data=PARAMS)
        res = req.json()
        
        print(res)
        return res


"""
    Identity Verifier
"""
def verify_wikiId(username, password):
    wikimedia_auth = WikimediaAuth()
    login_token = wikimedia_auth.get_API_token()
    login_res = wikimedia_auth.get_login(username, password, login_token)
    print(login_res)
        