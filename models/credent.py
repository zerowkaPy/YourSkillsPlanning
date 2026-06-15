from typing import Annotated
from pydantic import BaseModel,Field

class CredentModel(BaseModel):
    username:Annotated[str, Field(max_length=50)]
    email:Annotated[str, Field(max_length=255)]
    password:Annotated[str, Field(max_length=255)]

class LoginData(BaseModel):
    email:Annotated[str, Field(max_length=255)]
    password:Annotated[str, Field(max_length=255)]

class LinkData(BaseModel):
    token:Annotated[str, Field(max_length=128)]
    telegram_id:int