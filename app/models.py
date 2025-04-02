from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer)
    summary = db.Column(db.Text)

    def __repr__(self):
        return f'<Book {self.title}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)

    book = db.relationship('Book', backref='reviews')
    user = db.relationship('User', backref='reviews')

    def __repr__(self):
        return f'<Review {self.review_text[:20]}...>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'