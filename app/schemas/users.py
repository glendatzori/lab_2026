from sqlmodel import SQLModel, Field
from datetime import date

class BaseUser(SQLModel):
    name: str
    birth_date: date
    city: str

class UserDB(BaseUser, table=True):
    id: int = Field(default=None, primary_key=True)


class UserPublic(BaseUser):
    pass

