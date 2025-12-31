from flask import Blueprint, jsonify, request
from backend.app.schemas.payment import (
    PaymentCreateSchema, PaymentResponseSchema
)
from backend.app.services.payment_service import (
    create_payment,
    get_payment_by_id,
    get_payment_by_member,
    cancel_payment,
    get_all_payments
)

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

@payments_bp.get("/")
def get_all_payments_route():
    payments = get_all_payments()
    return jsonify([PaymentResponseSchema.from_orm(p).dict() for p in payments]), 200

@payments_bp.post("/")
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
def cancel_payment_route(payment_id):
    cancel_payment(payment_id)
    return jsonify({"message": "Payment canceled"}), 200