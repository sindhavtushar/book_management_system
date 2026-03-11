# app.views.books

from flask import Blueprint, render_template

views = Blueprint("views", __name__)

# templates render views
@views.route("/")
def home():
    return render_template("index.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/books/dashboard/")
def book_dashboard():
    return render_template("book-dashboard.html")

@views.route("/books/<id>/")
def book_detail(id):
    return render_template("book-detail.html", bookId = id)

@views.route("/author/<id>/")
def author_info(id):
    return render_template("author-details.html", author_id = id)

