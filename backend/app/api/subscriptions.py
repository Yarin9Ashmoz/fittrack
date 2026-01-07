from flask import Blueprint, request, jsonify

from backend.app.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionResponseSchema,
    SubscriptionUpdateEntriesSchema,
    SubscriptionFreezeSchema
)

from backend.app.services.subscription_service import (
    create_subscription,
    get_subscription_by_id,
    get_subscriptions_by_member,
    freeze_subscription,
    unfreeze_subscription,
    renew_subscription,
    update_remaining_entries,
    get_all_subscriptions
)

from backend.app.utils.security import roles_required, token_required

subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")

@subscriptions_bp.get("/")
@token_required
def get_all_subscriptions_route():
    subs = get_all_subscriptions()
    return jsonify([SubscriptionResponseSchema.from_orm(s).dict() for s in subs]), 200

@subscriptions_bp.post("/")
@token_required
@roles_required('admin', 'coach')
def create_subscription_route():
    data = request.get_json()
    subscription_data = SubscriptionCreateSchema(**data)
    new_subscription = create_subscription(subscription_data)
    return jsonify(SubscriptionResponseSchema.from_orm(new_subscription).dict()), 201

@subscriptions_bp.get("/<int:subscription_id>")
@token_required
def get_subscription_route(subscription_id):
    subscription = get_subscription_by_id(subscription_id)
    return jsonify(SubscriptionResponseSchema.from_orm(subscription).dict()), 200

@subscriptions_bp.get("/member/<int:member_id>")
@token_required
def get_member_subscriptions_route(member_id):
    subs = get_subscriptions_by_member(member_id)
    return jsonify([SubscriptionResponseSchema.from_orm(s).dict() for s in subs]), 200

@subscriptions_bp.put("/<int:subscription_id>/freeze")
@token_required
@roles_required('admin')
def freeze_subscription_route(subscription_id):
    data = request.get_json()
    freeze_data = SubscriptionFreezeSchema(**data)
    updated = freeze_subscription(subscription_id, freeze_data.frozen_until)
    return jsonify(SubscriptionResponseSchema.from_orm(updated).dict()), 200

@subscriptions_bp.put("/<int:subscription_id>/unfreeze")
@token_required
@roles_required('admin')
def unfreeze_subscription_route(subscription_id):
    updated = unfreeze_subscription(subscription_id)
    return jsonify(SubscriptionResponseSchema.from_orm(updated).dict()), 200

@subscriptions_bp.put("/<int:subscription_id>/renew")
@token_required
@roles_required('admin')
def renew_subscription_route(subscription_id):
    updated = renew_subscription(subscription_id)
    return jsonify(SubscriptionResponseSchema.from_orm(updated).dict()), 200

@subscriptions_bp.put("/<int:subscription_id>/update_entries")
@token_required
@roles_required('admin', 'coach')
def update_entries_route(subscription_id):
    data = request.get_json()
    update_data = SubscriptionUpdateEntriesSchema(**data)
    updated = update_remaining_entries(subscription_id, update_data.remaining_entries)
    return jsonify(SubscriptionResponseSchema.from_orm(updated).dict()), 200

