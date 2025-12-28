from flask import Flask, jsonify
from app.exceptions import (
    NotFoundError,
    DuplicateError,
    ValidationError,
    PermissionError,
    BusinessLogicError
)

app = Flask(__name__)

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404

@app.errorhandler(DuplicateError)
def handle_duplicate(e):
    return jsonify({"error": str(e)}), 409

@app.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": str(e)}), 400

@app.errorhandler(PermissionError)
def handle_permission(e):
    return jsonify({"error": str(e)}), 403

@app.errorhandler(BusinessLogicError)
def handle_business_logic(e):
    return jsonify({"error": str(e)}), 400
