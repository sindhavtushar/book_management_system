# app.views.books

from flask import Blueprint, render_template

views = Blueprint("views", __name__)

# templates render views
@views.route("/")
def home():
    return render_template("index.html")

@views.route("/books/dashboard/")
def book_dashboard():
    return render_template("book-dashboard.html")

@views.route("/books/<id>/")
def book_detail(id):
    return render_template("book-detail.html", bookId = id)

