from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from models.data_models import db, Author, Book
from datetime import datetime
from sqlalchemy.orm import joinedload

# Create Flask app
app = Flask(__name__)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
)

# Initialize database with app
db.init_app(app)


def sort_by(by):
    books = (
        db.session.query(Book)
        .join(Book.author)
        .options(joinedload(Book.author))
        .order_by(by)  # Author.name
        .all()
    )
    return books


# @app.route("/sort_by_author")
# def sort_by_author():
#     books = sort_by(Author.name)
#     return render_template("home.html", books=books)


# @app.route("/sort_by_title")
# def sort_by_title():
#     books = sort_by(Book.title)
#     return render_template("home.html", books=books)


@app.route("/sort")
def sort_books():
    sorted_by = request.args.get("by", "choice")
    if sorted_by == "author":
        choice = Author.name
    else:
        choice = Book.title

    books = sort_by(choice)
    return render_template("home.html", books=books)


@app.route("/home", methods=["GET"])
def home():
    books = (
        db.session.query(Book).join(Book.author).options(joinedload(Book.author)).all()
    )
    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        # add a new author record to the database
        name = request.form.get("name", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        date_of_death = request.form.get("date_of_death", None).strip()
        try:
            date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d").date()
        except ValueError:
            date_of_death = None

        author1 = Author(
            name=name,
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            date_of_death=date_of_death,
        )
        db.session.add(author1)
        db.session.commit()
        return redirect(url_for("home"))
        # return "Author successfully added to the database!"

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        # add a new book record to the database
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year = request.form.get("publication_year", "").strip()
        author_id = request.form.get("author_id", "").strip()
        # append new data to database
        book1 = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id,
        )

        db.session.add(book1)
        db.session.commit()
        return redirect(url_for("home"))
        # return "Book successfully added to the database!"

    return render_template("add_book.html", authors=db.session.query(Author).all())


@app.route("/book/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):

    book = Book.query.get_or_404(book_id, description="The book not found!")
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


# # Create tables
# with app.app_context():
#     db.create_all()

# Confirm table existence by querying
# authors = Author.query.all()
# print("Authors table is ready. Found:", len(authors), "records.")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)


# name = 'John Ronald Reuel Tolkien',
#         birth_date = '1892-01-03',
#         date_of_death = '1973-09-02',
