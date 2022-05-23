# FastAPI related
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Optional, List
from typing import Union
from fastapi.encoders import jsonable_encoder

# https://pydantic-docs.helpmanual.io/
from pydantic import BaseModel

# import scraper
import scraper as m_scraper


# data model class for request
class Item(BaseModel):
    url: str


class ItemList(BaseModel):
    urls: List[str]


class ItemExtracted(BaseModel):
    url: str
    extracted_data: List[str] = []



app = FastAPI(
    title='Website HREF Language Scraper',
    description= 'API for extracting HREF languages mentioned on a website',
    version= "1.0.0"
)


"""

    returns href language extracted and processed information

"""
@app.post("/extract-single")
def extract_hreflang_info(item: Item):
    
   # call scraper
    result = m_scraper.href_lang_scraper(item.url)
    return result


"""

    processed multiple urls

"""
@app.post("/extract-multiple")
def extract_hreflang_info_multiple_urls(item: ItemList):

    if len(item.urls) == 0:
        return {
            'status': 'error',
            'reason': 'empty list'
        }

    # call scraper on list
    combined_result = []
    
    for i in item.urls:
        result = m_scraper.href_lang_scraper(i.url)
