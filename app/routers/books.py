from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import BookCreate, BookPublic, BookDB
from typing import Annotated
from schemas.review import Review   #importiamo la classe dall'altro file
from data.db import SessionDep
from sqlmodel import select, delete


books_router = APIRouter(prefix="/books", tags=["books"])

"""
@books_router.get("/")
def get_all_books() -> list[Book]:
    Returns the list ok available books.
    return list(books.values())   #books.values è un generatore
"""
#riscriviamo questa get con le query strings
@books_router.get("/")
def get_all_books(
        session: SessionDep,
        sort: Annotated[bool, Query(description="Sort books by their review")] = False
) -> list[BookPublic]:
    """Returns the list ok available books."""
    # books è una lista di libri
    books = session.exec(select(BookDB)).all() #per prendere la lista di tutti i libri
    if sort:
        return sorted(books, key=lambda book: book.review)    #key è il campo che dovrebbe usare per ordinare la lista, lamba functions verrà applicata a ogni elemento di questa lista
    else:                                     #lamba prendono un input e restituiscono un output (dato un libro, prende il campo review)
        return list(books)


@books_router.get("/{id}")    #una GET per prendere un libro specifico, per questo usiamo /{id}
def get_book_by_id(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to retrieve")]      #parametro di percorso quindi mettiamo Path da fastapi
) -> BookPublic:
    """Returns the book with the given id"""
    book = session.get(BookDB, id)   #prendo un libro specifico, dato il suo id
    if book:
        return book
    else:
        return HTTPException(status_code=404, detail="Book not found")

#aggiungiamo l'ENDPOINT
@books_router.post("/{id}/review")
def add_review(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to retrieve")],
        review: Review
):
    """Add review to the book with the given ID"""
    book = session.get(BookDB, id)
    if not book: #se il libro non esiste
        raise HTTPException(status_code=404, detail="Book not found")
    book.review = review.review
    session.add(book) #rimpiazziamo la vecchia riga di database con quella nuova
    session.commit()
    return "Review added successfully"

@books_router.post("/")
def add_book(session: SessionDep, book: BookCreate):
    """Adds a new book."""
    book_entry = BookDB.model_validate(book)
    session.add(book_entry)
    session.commit()  #salviamo i cambiamenti
    return "Book added successfully"


@books_router.put("/{id}")
def replace_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to replace")],
        new_book: BookCreate
):
    """Replaces the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.add(book)
    session.commit()
    return "Book replaced successfully"

@books_router.delete("/")   #cancelliamo tutti i libri
def delete_all_books(session: SessionDep):
    """Deletes all the stored books"""
    session.exec(delete(BookDB))
    session.commit()
    return "All books deleted successfully"


@books_router.delete("/{id}")   #cancelliamo un solo libro
def delete_book(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the book to delete")],
):
    """Deletes the book with the given id"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return "Book deleted successfully"