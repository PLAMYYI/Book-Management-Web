import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User

with app.app_context():

    if User.query.filter_by(username="admin").first():
        print("Admin already exists")
        exit()

    admin = User(
        username="admin",
        email="admin@gmail.com",
        roles="admin,user"
    )

    admin.set_password("123456")

    db.session.add(admin)
    db.session.commit()

    print("Admin created!")