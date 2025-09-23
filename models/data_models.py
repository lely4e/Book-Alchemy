from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Author name: (name = {self.name})"


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    author_id = db.Column(
        db.Integer, db.ForeignKey("authors.author_id"), nullable=False
    )

    def __repr__(self):
        return f"Book: (title = {self.title}), ISBN: (isbn = {self.isbn})"
