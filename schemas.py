from pydantic import BaseModel
from typing import Optional

class Create(BaseModel):
    name: str
    gender: str
    age: Optional[int] = None

class Data(BaseModel):
    name:str
    age:int

class Show(BaseModel):
    data:Data

class User(BaseModel):
    name:str
    email:str
    password:str

class PassRes(BaseModel):
    name:str
    email:str

class Authenticate(BaseModel):
    password: str
    email: str