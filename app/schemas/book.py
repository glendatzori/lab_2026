#STRUTTURA DATI PER L'OGGETTO LIBRO

from pydantic import BaseModel
from typing import Annotated
from sqlmodel import SQLModel, Field

# si devono prima validare i dati e poi si salvano nel database
class BookBase(SQLModel): #le altre classi erediteranno questi attributi
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)] = None
class BookCreate(BookBase):
    pass
class BookPublic(BookBase):  #schema utilizzato nelle get, (ci dovrà essere l'id)
    id: int

class BookDB(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key='User.id')


