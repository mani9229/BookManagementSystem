from marshmallow import Schema, fields, post_load, validate

from app.models import Book, Review, User

class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    genre = fields.String(required=True)
    year_published = fields.Integer()
    summary = fields.String()

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)

class ReviewSchema(Schema):
    id = fields.Integer(dump_only=True)
    book_id = fields.Integer(required=True)
    user_id = fields.Integer(dump_only=True)  # Don't allow user_id to be passed in
    review_text = fields.String()
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))

    @post_load
    def make_review(self, data, **kwargs):
        return Review(**data)

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)  # Only for input, not output

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)