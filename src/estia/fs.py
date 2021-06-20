"""
    Interacting with the IPFS API. 
"""
import ipfsApi
from config import ConfigParams

def get_api_con():
    api = ipfsApi.Client(ConfigParams.IPFS_API, ConfigParams.IPFS_PORT)
    return api

