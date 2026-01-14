from flask import Blueprint, request, jsonify
from backend.app.db.database import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app.utils.security import generate_token
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with SessionLocal() as session:
        user_repo = UserRepository(session)
        user = user_repo.get_by_email(email)

        if not user or not user.password_hash:
            return jsonify({"error": "Invalid credentials"}), 401
        
        try:
            if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                 return jsonify({"error": "Invalid credentials"}), 401
        except Exception:
            # Fallback for plain text during migration/seeding if needed
            if password != user.password_hash:
                return jsonify({"error": "Invalid credentials"}), 401

        token = generate_token(user.id)
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
