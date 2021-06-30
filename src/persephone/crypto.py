# Since FastAPI does not sign cookies with HMAC we need to do
# the process. 
import hmac
import hashlib

from config import ConfigParams

class Cookie:
    

    def sign(self, cookie_value):
        signature = hmac.new(str.encode(ConfigParams.HMAC_SIGN_KEY), str.encode(cookie_value), hashlib.sha256).hexdigest()
        return signature
    
    
    def verify(self, cookie_value):
        if cookie_value == self.sign(cookie_value):
            return True
        else:
            return False
          