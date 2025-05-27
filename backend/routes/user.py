from datetime import datetime

from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from pydantic_core._pydantic_core import ValidationError

from backend.models import db, User
from backend.validators import LoginValidator


class UserResource(Resource):
    @jwt_required(optional=True)
    def __init__(self):
        self.user = None
        if get_jwt_identity():
            self.user = User.query.get(User.get_id_from_identity(get_jwt_identity()))

    def get(self):
        if self.user is None:
            return {"status": "unauthorized"}, 401
        return {'status': 'success', 'user': self.user.to_json()}, 200

    def post(self):
        if self.user is not None:
            return {"status": "alreadyLoggedIn"}, 403
        data = request.form
        try:
            data = LoginValidator(**data)
        except ValidationError as err:
            return {"status": "failed", "errors": err.json()}, 400
        action = request.args.get("action")
        if action == "login":
            # Checking multiple login methods
            user = User.query.filter(User.email == data.login).first()
            if user is None or not user.check_login(data.password):
                return {"status": "unauthorized"}, 401

            user.last_login_at = datetime.now()

            identity = user.make_identity()
            access_token = create_access_token(identity)
            refresh_token = create_refresh_token(identity)

            db.session.commit()

            return {'status': 'success', 'user': user.to_json(), 'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }}, 200
        return {"status": "badData"}, 400