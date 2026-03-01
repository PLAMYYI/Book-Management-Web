from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User ,Book
from forms import RegisterForm, LoginForm

app = Flask(__name__)

# ================= CONFIG =================
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ================= LOGIN MANAGER =================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= ROUTES =================

@app.route("/")
@login_required
def index():

    if current_user.has_roles(["admin"]):
        books = Book.query.all()
    else:
        books = Book.query.filter_by(user_id=current_user.id).all()

    return render_template("main/index.html", books=books)


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # เช็ค email ซ้ำ
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already exists")
            return redirect(url_for("register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            roles=form.roles.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Register successful! Please login.")
        return redirect(url_for("login"))

    return render_template("accounts/register.html", form=form)


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password")

    return render_template("accounts/login.html", form=form)


# ---------- LOGOUT ----------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("index"))


# ---------- ADD BOOK ----------
@app.route("/add-book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")

        if not title or not author:
            flash("Please fill in all fields")
            return redirect(url_for("add_book"))

        new_book = Book(
            title=title,
            author=author,
            user_id=current_user.id   # 🔥 เพิ่มบรรทัดนี้
        )

        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully!")
        return redirect(url_for("index"))

    return render_template("main/add_book.html")

# ---------- DELETE BOOK ----------
@app.route("/delete-book/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):

    book = Book.query.get_or_404(book_id)

    # 🔒 กันลบของคนอื่น (ยกเว้น admin)
    if not current_user.has_roles(["admin"]) and book.user_id != current_user.id:
        flash("You are not allowed to delete this book.")
        return redirect(url_for("index"))

    db.session.delete(book)
    db.session.commit()

    flash("Book deleted successfully!")
    return redirect(url_for("index"))

# ---------- EDIT BOOK ----------
@app.route("/edit-book/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):

    book = Book.query.get_or_404(book_id)

    # 🔒 กันแก้ของคนอื่น (ยกเว้น admin)
    if not current_user.has_roles(["admin"]) and book.user_id != current_user.id:
        flash("You are not allowed to edit this book.")
        return redirect(url_for("index"))

    if request.method == "POST":
        book.title = request.form.get("title")
        book.author = request.form.get("author")

        db.session.commit()
        flash("Book updated successfully!")
        return redirect(url_for("index"))

    return render_template("main/edit_book.html", book=book)


# ================= MAIN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)