from flask import Blueprint, request, jsonify
from app.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionUpdateSchema,
    SubscriptionResponseSchema
)
from app.services.subscription_service import create_subscription


subscriptions_bp = Blueprint("subscriptions", __name__)

@subscriptions_bp.post("/")
def create_subscription_route():
    data = request.get_json()
    subscription_data = SubscriptionCreateSchema(**data)
    new_subscription = create_subscription(subscription_data)
    return jsonify(SubscriptionResponseSchema.from_orm(new_subscription).dict()), 201

