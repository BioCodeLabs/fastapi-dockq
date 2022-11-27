from pydantic import BaseModel

class payloadScheme(BaseModel):
    pay_01:str
    pay_02:str
    pay_03:str
    pay_04:str
    pay_05:str

    class Config:
	    orm_mode = True
