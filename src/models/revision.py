import json
from pydantic import BaseModel

class WikiRevision(BaseModel):
    content: str
