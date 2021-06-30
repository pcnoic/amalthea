"""
    config.py

    Configuration values for Amalthea
    
    GNU GENERAL PUBLIC LICENSE
"""

# TODO: make this read params from environment variables
class ConfigParams:
    WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
    WIKIPEDIA_DOMAIN = "en.wikipedia.org"
    XTOOLS_API_URL = "https://xtools.wmflabs.org/api/page/articleinfo"
    MONGODB_HOST = "mongodb://localhost:27017" # MongoDB host: can also have basic auth
    MONGODB_DBNAME = "xenia"
    MAX_WIKIPEDIA_REV = 1000
    HMAC_SIGN_KEY = "xenia"
    
    