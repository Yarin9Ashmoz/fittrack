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
from backend.app.api.intake_evaluations import intake_evaluations_bp
from backend.app.api.personal_tracking import personal_tracking_bp
from backend.app.api.error_reports import error_reports_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Ensure database schema is up-to-date (add new columns/backfills if needed)
    from backend.app.db.database import create_all_tables
    create_all_tables()

    # Register blueprints
    from backend.app.api.auth import auth_bp
    app.register_blueprint(auth_bp)

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
    
    # New feature blueprints
    app.register_blueprint(intake_evaluations_bp)
    app.register_blueprint(personal_tracking_bp)
    app.register_blueprint(error_reports_bp)


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

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5005, debug=False)
