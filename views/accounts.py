from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db
from forms import RegisterForm, LoginForm

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("สมัครสมาชิกสำเร็จ")
        return redirect(url_for("accounts.login"))
    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Email หรือ Password ไม่ถูกต้อง")
    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))