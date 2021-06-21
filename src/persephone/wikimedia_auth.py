"""
    OAuth owner-only consumers authenticating against WikiPedia's API
"""

from fastapi import responses
from fastapi_users import user
import requests
from config import ConfigParams
import json


class WikimediaAuth:

    S = requests.Session()
    URL = ConfigParams.WIKIPEDIA_API_URL

    def start_client_login(self, username, password):
        """
            Send a post request along with login token,
            user information and return URL to the API 
            to log in on a wiki
        """
        login_token = self.fetch_login_token()
        session = self.S

        response = session.post(url=self.URL, data={
            'action': "clientlogin",
            'username': username,
            'password': password,
            'loginreturnurl': "http://localhost:8000/",
            'logintoken': login_token,
            'format': "json"
        })
        
        # print(response.content)
        data = json.loads(response.content)
        
        if data['clientlogin']['status'] == 'PASS':
            # Handle success
            print("Successful login for WikiPedia user {user}".format(
                user = data['clientlogin']['username']
            ))
            return data['clientlogin']['username']
        else:
            # Handle failure
            print("Something went wrong when trying to login with {user} and {password}".format(
                user = username,
                password = password
            ))
            return 1

    def fetch_login_token(self):
        """ Fetch login token via 'tokens' module """
        session = self.S
        response = session.get(
            url=self.URL,
            params={
                'action': "query",
                'meta': "tokens",
                'type': "login",
                'format': "json"
                }
        )
        data = response.json()
        token = data['query']['tokens']['logintoken']
        print("Received token " + token) 
        return token

"""
    Identity Verifier
"""
def get_wikiId(username, password):
    wikimedia_auth = WikimediaAuth()
    wiki_user = wikimedia_auth.start_client_login(username, password)
    if wiki_user != 1:
        return wiki_user
    else:
        return 1
        