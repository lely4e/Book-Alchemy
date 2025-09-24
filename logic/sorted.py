from flask_sqlalchemy import SQLAlchemy
from models.data_models import db, Author, Book
from sqlalchemy.orm import joinedload
from sqlalchemy import or_


def sort_by(by):
    """Books sorted by title or author"""
    books = (
        db.session.query(Book)
        .join(Book.author)
        .options(joinedload(Book.author))
        .order_by(by)
        .all()
    )
    return books


def search_by(text):
    """Books sorted based on the search"""
    books = (
        db.session.query(Book)
        .join(Book.author)
        .options(joinedload(Book.author))
        .filter(or_(Author.name.ilike(f"%{text}%"), Book.title.ilike(f"%{text}%")))
        .all()
    )
    return books
