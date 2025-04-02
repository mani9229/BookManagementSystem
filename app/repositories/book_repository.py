from app import db
from app.models import Book
from typing import List, Optional

def get_all_books() -> List[Book]:
    """
    Retrieves all books from the database.
    """
    return Book.query.all()

def get_book_by_id(book_id: int) -> Optional[Book]:
    """
    Retrieves a specific book by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.

    Returns:
        Optional[Book]: The book object, or None if not found.
    """
    return Book.query.get(book_id)

def create_book(book_data: dict) -> Book:
    """
    Creates a new book in the database.

    Args:
        book_data (dict): A dictionary containing the book's data 
                         (title, author, genre, year_published, summary).

    Returns:
        Book: The newly created book object.
    """
    new_book = Book(**book_data)
    db.session.add(new_book)
    db.session.commit()
    return new_book

def update_book(book_id: int, book_data: dict) -> Optional[Book]:
    """
    Updates a book's information in the database.

    Args:
        book_id (int): The ID of the book to update.
        book_data (dict): A dictionary containing the updated book data.

    Returns:
        Optional[Book]: The updated book object, or None if not found.
    """
    book = get_book_by_id(book_id)
    if book:
        for key, value in book_data.items():
            setattr(book, key, value)
        db.session.commit()
        return book
    return None

def delete_book(book_id: int) -> bool:
    """
    Deletes a book from the database.

    Args:
        book_id (int): The ID of the book to delete.

    Returns:
        bool: True if the book was deleted, False if not found.
    """
    book = get_book_by_id(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return True
    return False