from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from logic.sorted import sort_by, search_by
from models.data_models import db, Author, Book
import os
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


@app.route("/search", methods=["GET"])
def search_books():
    """Search books by author name or by title"""
    search_text = request.args.get("search", "")
    books = search_by(search_text)
    if not books:
        return render_template("home.html", books=books, message="No books found!")
    return render_template("home.html", books=books)


@app.route("/sort")
def sort_books():
    """Sort books by author name or by title"""
    sorted_by = request.args.get("by", "title")
    if sorted_by == "author":
        choice = Author.name
    else:
        choice = Book.title

    books = sort_by(choice)
    return render_template("home.html", books=books)


@app.route("/home", methods=["GET"])
def home():
    """Home page represents all books"""
    books = (
        db.session.query(Book).join(Book.author).options(joinedload(Book.author)).all()
    )
    if books:
        return render_template(
            "home.html", books=books, message=request.args.get("message", None)
        )
    else:
        return render_template(
            "home.html", books=[], message="There are no books found"
        )


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """Adds a new author to the database.

    GET: display the form.
    POST: process the form submission, validates input and redirects
    to the homepage.
    """
    if request.method == "POST":
        # add a new author record to the database
        name = request.form.get("name", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        date_of_death = request.form.get("date_of_death", None).strip()

        if not name or not birth_date:
            return render_template(
                "add_author.html", error="Name or Birth Date missing"
            )

        try:
            date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d").date()
        except ValueError:
            date_of_death = None

        author = Author(
            name=name,
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            date_of_death=date_of_death,
        )
        db.session.add(author)
        db.session.commit()
        return redirect(url_for("home", message="Author was added successfully"))

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Adds a new book to the database.

    GET: display the form.
    POST: process the form submission, validates input and redirects
    to the homepage.
    """
    if request.method == "POST":
        # add a new book record to the database
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year = request.form.get("publication_year", "").strip()
        author_id = request.form.get("author_id", "").strip()
        # append new data to database
        book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id,
        )

        db.session.add(book)
        db.session.commit()
        return redirect(url_for("home", message="Book was added successfully"))

    return render_template("add_book.html", authors=db.session.query(Author).all())


@app.route("/book/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    """Deletes book if it's exist, otherwise it shows error"""
    book = Book.query.get_or_404(book_id, description="The book not found!")
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if not Book.query.filter_by(author_id=author.author_id).count():
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for("home", message="Book and it's author were deleted"))

    return redirect(url_for("home", message="Book was deleted successfully"))


if __name__ == "__main__":
    # # Create tables
    # with app.app_context():
    #     db.create_all()
    app.run(host="127.0.0.1", port=5001, debug=True)
