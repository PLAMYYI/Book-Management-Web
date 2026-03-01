from .main import module as main_module
from .accounts import accounts

def register_blueprint(app):
    app.register_blueprint(main_module)
    app.register_blueprint(accounts_module)