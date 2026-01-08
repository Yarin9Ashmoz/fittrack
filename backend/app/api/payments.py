from flask import Blueprint, jsonify, request
from backend.app.schemas.payment import (
    PaymentCreateSchema, PaymentResponseSchema
)
from backend.app.services.payment_service import (
    create_payment,
    get_payment_by_id,
    get_payment_by_member,
    cancel_payment,
    get_all_payments,
    calculate_payment_for_closed_class,
    process_subscription_payment,
    mark_payment_as_paid,
    get_pending_payments
)
from backend.app.utils.security import token_required, roles_required

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

@payments_bp.get("/")
@token_required
def get_all_payments_route():
    # TODO: Filter by permissions
    payments = get_all_payments()
    return jsonify([PaymentResponseSchema.from_orm(p).dict() for p in payments]), 200

@payments_bp.post("/")
@token_required
def create_payment_route():
    data = request.get_json()
    payment_data = PaymentCreateSchema(**data)
    new_payment = create_payment(payment_data)
    return jsonify(PaymentResponseSchema.from_orm(new_payment).dict()), 201

@payments_bp.get("/<int:payment_id>")
def get_payment_by_id_route(payment_id):
    payment = get_payment_by_id(payment_id)
    return jsonify(PaymentResponseSchema.from_orm(payment).dict()), 200

@payments_bp.get("/member/<int:member_id>")
def get_payment_by_member_route(member_id):
    payments = get_payment_by_member(member_id)
    return jsonify([PaymentResponseSchema.from_orm(p).dict() for p in payments]), 200

@payments_bp.delete("/<int:payment_id>")
@token_required
@roles_required('admin')
def cancel_payment_route(payment_id):
    cancel_payment(payment_id)
    return jsonify({"message": "Payment canceled"}), 200

@payments_bp.post("/calculate-for-class/<int:class_id>")
@token_required
@roles_required('admin')
def calculate_class_payment_route(class_id):
    """Calculate payment for a closed class (admin only)"""
    data = request.get_json() or {}
    trainer_id = data.get('trainer_id')
    amount = data.get('amount', 50.0)
    
    if not trainer_id:
        return jsonify({"error": "trainer_id is required"}), 400
    
    payment = calculate_payment_for_closed_class(class_id, trainer_id, amount)
    return jsonify(PaymentResponseSchema.from_orm(payment).dict()), 201

@payments_bp.post("/process-subscription/<int:subscription_id>")
@token_required
@roles_required('admin')
def process_subscription_payment_route(subscription_id):
    """Process subscription payment (admin only)"""
    data = request.get_json() or {}
    amount = data.get('amount')
    
    if not amount:
        return jsonify({"error": "amount is required"}), 400
    
    payment = process_subscription_payment(subscription_id, amount)
    return jsonify(PaymentResponseSchema.from_orm(payment).dict()), 201

@payments_bp.post("/<int:payment_id>/mark-paid")
@token_required
@roles_required('admin')
def mark_payment_paid_route(payment_id):
    """Mark a payment as completed (admin only)"""
    payment = mark_payment_as_paid(payment_id)
    return jsonify(PaymentResponseSchema.from_orm(payment).dict()), 200

@payments_bp.get("/pending")
@token_required
@roles_required('admin')
def get_pending_payments_route():
    """Get all pending payments (admin only)"""
    payments = get_pending_payments()
    return jsonify([PaymentResponseSchema.from_orm(p).dict() for p in payments]), 200