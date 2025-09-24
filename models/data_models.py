from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Representing an Author.

    Attributes:
        author_id (int): Primary key.
        name (str): Author's name.
        birth_date (date): Author's birth date.
        date_of_death (date): Author's birth date if exists.
    """

    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Author name: {self.name}"


class Book(db.Model):
    """Representing a Book.

    Attributes:
        book_id (int): Primary key.
        isbn (str): Book's ISBN.
        title (str): Book's title.
        publication_year (int): Book's publication year.
        author_id (int): Foreign key.
    """

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey("authors.author_id", ondelete="CASCADE"),
        nullable=False,
    )

    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}"
