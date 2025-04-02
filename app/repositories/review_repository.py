from app import db
from app.models import Review
from typing import List, Optional

def get_reviews_by_book_id(book_id: int) -> List[Review]:
    """
    Retrieves all reviews for a specific book.

    Args:
        book_id (int): The ID of the book to get reviews for.

    Returns:
        List[Review]: A list of Review objects.
    """
    return Review.query.filter_by(book_id=book_id).all()


def get_review_by_id(review_id: int) -> Optional[Review]:
    """
    Retrieves a specific review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.

    Returns:
        Optional[Review]: The Review object, or None if not found.
    """
    return Review.query.get(review_id)


def create_review(book_id: int, user_id: int, review_text: str, rating: int) -> Review:
    """
    Creates a new review for a book.

    Args:
        book_id (int): The ID of the book being reviewed.
        user_id (int): The ID of the user writing the review.
        review_text (str): The text of the review.
        rating (int): The rating given for the book.

    Returns:
        Review: The newly created Review object.
    """
    new_review = Review(book_id=book_id, user_id=user_id, review_text=review_text, rating=rating)
    db.session.add(new_review)
    db.session.commit()
    return new_review


def update_review(review_id: int, review_data: dict) -> Optional[Review]:
    """
    Updates a review's information.

    Args:
        review_id (int): The ID of the review to update.
        review_data (dict): A dictionary containing the updated review data 
                           (review_text, rating).

    Returns:
        Optional[Review]: The updated Review object, or None if not found.
    """
    review = get_review_by_id(review_id)
    if review:
        for key, value in review_data.items():
            setattr(review, key, value)
        db.session.commit()
        return review
    return None


def delete_review(review_id: int) -> bool:
    """
    Deletes a review.

    Args:
        review_id (int): The ID of the review to delete.

    Returns:
        bool: True if the review was deleted, False if not found.
    """
    review = get_review_id(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False