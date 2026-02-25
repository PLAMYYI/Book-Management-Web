import os
from flask import Flask
from extensions import db, login_manager
from views import init_app

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)