from faker import Faker

from backend.models import User
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

fake = Faker()


class Seeder:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_user(self, default=True):
        name = fake.name()
        password = generate_password_hash("testpass")
        if default and User.query.filter_by(email="test@email.com").count():
            return None
        self.db.session.add(
            User(
                username=name.split()[0],
                email=fake.email() if not default else "test@email.com",
                password=password
            )
        )
        self.db.session.commit()