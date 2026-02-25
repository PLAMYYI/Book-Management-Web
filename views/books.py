from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Book
from extensions import db
from forms import BookForm

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(book)
        db.session.commit()
        flash("เพิ่มหนังสือสำเร็จ")
        return redirect(url_for("main.index"))
    return render_template("books/create.html", form=form)


@books_bp.route("/<int:id>")
def detail(id):
    book = Book.query.get_or_404(id)
    return render_template("books/detail.html", book=book)