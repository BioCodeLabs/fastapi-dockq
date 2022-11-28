from typing import List
from pydantic import BaseModel

class payloadScheme(BaseModel):
    pay_01:str
    pay_02:str
    pay_03:str
    pay_04:str
    pay_05:str
    pay_06:str
    pay_07:str
    pay_08:str
    pay_09:str
    pay_10:str



    class Config:
	    orm_mode = True

class dataPayloadScheme(BaseModel):
    data: List=[]