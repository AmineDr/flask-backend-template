import math
import time
from datetime import datetime
from threading import Thread

from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from backend.models import User, RootUser, LikedProduct, Product, db
from backend.validators import LoginValidator, RegisterValidator
from backend.utils import check_privilege


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
        action = request.args.get("action")
        if action != "register":
            action = "login"
        try:
            data = RegisterValidator(**data) if action == "register" else LoginValidator(**data)
        except ValidationError as err:
            return {"status": "badData", "message": [f"{x.get('msg')}: {x.get('loc')[0]}" for x in err.errors()]}, 400
        except Exception as e:
            abort(500, str(e))
        if action == "login":
            # Checking multiple login methods
            user = User.query.filter(User.email == data.login).first()
            if user is None or not user.check_login(data.password):
                return {"status": "unauthorized"}, 401

            user.last_login_at = datetime.now()
            user.active = True

            identity = user.make_identity()
            access_token = create_access_token(identity)
            refresh_token = create_refresh_token(identity)

            db.session.commit()

            return {'status': 'success', 'user': user.to_json(), 'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }}, 200
        elif action == "register":
            try:
                user = User(**data.__dict__)
                user.gen_pass()
                user.gen_user_id()

                identity = user.make_identity()
                access_token, refresh_token = create_access_token(identity), create_refresh_token(identity)

                db.session.add(user)
                db.session.commit()

                self.user = user

                return {"status": "registered", "user": user.to_json(), "tokens": {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }}, 200

            except IntegrityError as err:
                str_err = str(err.__dict__['orig']).lower()
                if str_err.find('duplicate entry') != -1:
                    if str_err.find("username") != -1:
                        return {"status": "error", "message": "User already exists"}, 400
                    elif str_err.find("email") != -1:
                        return {"status": "error", "message": "Email exists"}, 400
                    elif str_err.find("phone") != -1:
                        return {"status": "error", "message": "Phone already exists"}, 400
                print(err.__dict__['orig'])
                return {"status": "error"}, 400

            except Exception as e:
                print(e)
                return {"status": "error", "message": "Error registering the user"}, 400
