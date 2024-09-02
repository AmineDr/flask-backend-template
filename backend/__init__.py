import os.path
import json

from flask import Flask, abort, request, send_from_directory, url_for, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy.exc import IntegrityError

from backend.config import Config
from backend.errors import InvalidConfigError
from backend.models import *
from backend.routes.user import UserResource
from backend.seeds import Seeder
from backend.utils import PrivilegeService

app = Flask(__name__)

if not app.get('FLASK_SECRET_KEY'):
    raise InvalidConfigError
else:
    app.config.from_object(Config)

app.static_folder = os.environ.get("STATIC_FOLDER")

black_list = set()

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app, prefix='/api/')

# Registering API Routes
from backend.routes import *
api.add_resource(UserResource, 'users')

if app.config.get('ENV') == "production":
    CORS(app, resources={r"/api/*": {"origins": [app.config.get('SERVER_HOST')]}})
else:
    CORS(app)

seeder = Seeder(db)

with open('./secrets/oauth.json') as f:
    google_secrets = json.load(f)


with app.app_context():
    db.create_all()
    seeder.create_user(default=True)


@app.route('/static/<path:directory>/<path:filename>')
def static_serve(directory, filename):
    relative_path = os.path.join(directory, filename)
    file_path = os.path.join(os.environ.get('STATIC_FOLDER'), relative_path)

    path, filename = os.path.split(os.path.abspath(file_path))
    if not os.path.exists(path):
        abort(404)
    return send_from_directory(path, filename)


@app.route('/api')
def home():
    server_name = app.config.get('SERVER_SHORT_NAME')
    return {
        "status": "success",
        "message": f"Welcome to {server_name} API"
    }


@app.route('/api/logout', methods=['DELETE'])
@jwt_required(optional=True)
def logout():
    identity = get_jwt_identity()
    try:
        token = RevokedToken(token=identity)
        db.session.add(token)
        db.session.commit()
        return {"status": "success"}, 204
    except IntegrityError:
        return {"status": "alreadyLoggedOut"}, 403


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    return RevokedToken.query.filter_by(token=jti).count() >= 1


@app.route('/api/ping')
def ping():
    return "Pong"


@app.route('/api/cause_error')
def cause_error():
    if app.config.VARS.get('ENV') == "development":
        abort(500)
    abort(404)


@app.errorhandler(404)
def handle_not_found(*args):
    return {
        "status": "NotFound"
    }


@app.errorhandler(500)
def handle_server_error(err):
    return {
        "status": "error",
        "message": str(err)
    }


@app.route("/api/refresh", methods=["PUT"])
@jwt_required(refresh=True)
def refresh():
    return {
        "access_token": create_access_token(identity=get_jwt_identity())
    }
