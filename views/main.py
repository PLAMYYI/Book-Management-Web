from ast import main
from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("main/index.html")

@main.route("/add-book", methods=["GET", "POST"])
def add_book():
    return render_template("main/add_book.html")