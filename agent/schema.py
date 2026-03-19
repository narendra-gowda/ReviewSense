from pydantic import BaseModel
from utils.constants import Platform

class ReviewQueryInput(BaseModel):
    query: str
    platform: Platform
    app_name: str

class QueryInput(BaseModel):
    query: str