from .main import main_bp
from .accounts import accounts_bp
from .books import books_bp

def init_app(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(books_bp)