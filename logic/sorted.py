from flask_sqlalchemy import SQLAlchemy
from models.data_models import db, Author, Book
from sqlalchemy.orm import joinedload


def sort_by(by):
    books = (
        db.session.query(Book)
        .join(Book.author)
        .options(joinedload(Book.author))
        .order_by(by)  # Author.name
        .all()
    )
    return books
