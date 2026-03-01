from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Book
from acl import role_required

module = Blueprint("books", __name__, url_prefix="/books")


# ================= LIST BOOKS =================
@module.route("/")
@login_required
def list_books():

    # 👑 Admin เห็นทุกเล่ม
    if current_user.has_roles(["admin"]):
        books = Book.query.all()
    else:
        # 👤 User เห็นเฉพาะของตัวเอง
        books = Book.query.filter_by(user_id=current_user.id).all()

    return render_template("books/list.html", books=books)


# ================= ADD BOOK =================
@module.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")

        # ป้องกันกรอกว่าง
        if not title or not author:
            flash("Please fill in all fields.")
            return redirect(url_for("books.add_book"))

        new_book = Book(
            title=title,
            author=author,
            user_id=current_user.id
        )

        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully!")
        return redirect(url_for("books.list_books"))

    return render_template("main/add_book.html")