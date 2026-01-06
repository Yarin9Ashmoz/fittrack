from flask import Flask, jsonify
from flask_cors import CORS

# Error classes
from backend.app.exceptions import (
    NotFoundError,
    DuplicateError,
    ValidationError,
    PermissionError,
    BusinessLogicError
)

# Blueprints
from backend.app.api.users import users_bp
from backend.app.api.plans import plans_bp
from backend.app.api.subscriptions import subscriptions_bp
from backend.app.api.checkins import checkins_bp
from backend.app.api.class_sessions import classes_bp
from backend.app.api.enrollments import enrollments_bp
from backend.app.api.payments import payments_bp
from backend.app.api.workout_plans import workout_plans_bp
from backend.app.api.workout_items import workout_items_bp
from backend.app.api.search import search_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(plans_bp)
    app.register_blueprint(subscriptions_bp)
    app.register_blueprint(checkins_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(workout_plans_bp)
    app.register_blueprint(workout_items_bp)
    app.register_blueprint(search_bp)

    # Error handlers
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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
