from flask_login import LoginManager, current_user
from flask import redirect, url_for
from functools import wraps
from models import User

login_manager = LoginManager()

def init_acl(app):
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def roles_required(roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("accounts.login"))

            if not current_user.has_roles(roles):
                return "Forbidden", 403

            return func(*args, **kwargs)
        return wrapped
    return wrapper