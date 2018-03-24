from flask import request
from flask_restful import Resource, abort
from cosmicpi.config import Config
from functools import wraps


TOKEN = '_'.join([Config.get('UI', 'username'), Config.get('UI', 'password')])


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in request.args or request.args['token'] != TOKEN:
            return abort(401)
        return f(*args, **kwargs)
    return decorated


class Auth(Resource):
    def get(self):
        if request.args['token'] != TOKEN:
            abort(401)
        return {'result': 'success', 'message': 'Username and password are correct'}
