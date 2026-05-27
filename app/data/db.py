from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from schemas.book import BookDB # noqa
from schemas.users import UserDB
from faker import Faker   #pip install faker
import os

sqlite_file_name = "C:\\Users\\glend\\lab_2026\\app\\data\\database.db"   #file persistente in memoria
sqlite_url = f"sqlite:///{sqlite_file_name}"    #file endpoint dove viene montato qualcosa(?)
engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False},
    echo=True
)

#inizializziamo il database
def init_database():
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                book = BookDB(
                    title=f.sentence(nb_words=5),
                    author=f.name(),
                    review=f.pyint(1,5),
                    user_id= f.pyint(1,10)
                )
                session.add(book)
            for i in range(10):
                user = UserDB(
                    name = f.name(),
                    birth_year = f.date_of_birth(),
                    city=f.city()
                )
            session.commit() #dentro il contex manager

#dependecies
def get_session():
    with Session(engine) as session: #apriamo la variabile con il contex manager (with)
        yield session

SessionDep = Annotated[Session, Depends(get_session)]   #questa variabile session è un'istanza di Session, e viene creata da get_session (quindi è una sessione del database)
