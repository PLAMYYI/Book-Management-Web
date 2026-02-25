from flask import Blueprint, render_template
from models import Book

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    books = Book.query.all()
    return render_template("main/index.html", books=books)