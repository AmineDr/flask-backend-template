from datetime import timedelta

from dotenv import load_dotenv
import os

load_dotenv()
env = os.environ

secret_key = env.get("FLASK_SECRET_KEY")
if secret_key is None:
    secret_key = "Secret-Sauce"

DB_USER = env.get("DB_USER")
DB_PASS = env.get("DB_PASS")
DB_NAME = env.get("DB_NAME")
DB_HOST = env.get("DB_HOST")
DB_PORT = env.get("DB_PORT")

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class Config:
    DEBUG = env.get("ENV") == "development"
    ENV = env.get("ENV") or "development"

    # SERVER_NAME = env.get("SERVER_NAME")
    SERVER_SHORT_NAME = env.get("SERVER_SHORT_NAME")

    HOST = env.get("SERVER_HOST") or "localhost"
    PORT = env.get("SERVER_PORT") or 5000

    SECRET_KEY = env.get('FLASK_SECRET_KEY')
    JWT_SECRET_KEY = env.get('FLASK_SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    STATIC_FOLDER = env.get('STATIC_FOLDER')
    UPLOAD_FOLDER = env.get("UPLOAD_FOLDER")

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = db_url

    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY = None
    SESSION_PERMANENT = False

    SERVER_PIN = env.get("SERVER_PIN")
    VARS = dict(env)
