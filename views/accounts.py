from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegisterForm, LoginForm
from acl import roles_required

accounts = Blueprint("accounts", __name__)


@accounts.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists")
            return render_template("accounts/register.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            roles=",".join(form.roles.data)
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Register success")
        return redirect(url_for("accounts.login"))

    return render_template("accounts/register.html", form=form)


@accounts.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Invalid credentials")

    return render_template("accounts/login.html", form=form)


@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("accounts.login"))


@accounts.route("/users")
@login_required
@roles_required(["admin"])
def users():
    all_users = User.query.all()
    return render_template("accounts/users.html", all_users=all_users)