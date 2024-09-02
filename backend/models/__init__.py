from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend.models.user import User


class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True)

