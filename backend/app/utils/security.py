import jwt
import datetime
from functools import wraps
from flask import request, jsonify, g
from backend.app.db.database import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app.exceptions import PermissionError

SECRET_KEY = "super-secret-key" # In production, use environment variable

def generate_token(user_id: int):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Allow preflight requests
        if request.method == "OPTIONS":
            return f(*args, **kwargs)

        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            with SessionLocal() as session:
                user = UserRepository(session).get_by_id(int(data['sub']))
                if not user:
                    return jsonify({'message': 'User not found!'}), 401
                g.user = user
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)
    return decorated


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user') or g.user.role not in roles:
                raise PermissionError(f"Role(s) {roles} required")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
