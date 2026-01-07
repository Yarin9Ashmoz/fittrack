from flask import Blueprint, request, jsonify
from backend.app.schemas.plan import (
    PlanCreateSchema,
    UpdatePlanSchema,
    PlanResponseSchema
)
from backend.app.services.plan_service import (
    create_plan,
    get_plan_by_id,
    get_all_plans,
    update_plan,
    delete_plan
)
from backend.app.exceptions import NotFoundError, ValidationError


from backend.app.utils.security import roles_required, token_required

plans_bp = Blueprint("plans", __name__, url_prefix="/plans")


@plans_bp.post("/")
@token_required
@roles_required('admin')
def create_plan_route():
    try:
        data = request.get_json()
        plan_data = PlanCreateSchema(**data)
        new_plan = create_plan(plan_data)
        return jsonify(PlanResponseSchema.from_orm(new_plan).dict()), 201

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@plans_bp.get("/")
@token_required
def get_all_plans_route():
    plans = get_all_plans()
    return jsonify([PlanResponseSchema.from_orm(p).dict() for p in plans]), 200


@plans_bp.get("/<int:plan_id>")
@token_required
def get_plan_route(plan_id):
    try:
        plan = get_plan_by_id(plan_id)
        return jsonify(PlanResponseSchema.from_orm(plan).dict()), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@plans_bp.put("/<int:plan_id>")
@token_required
@roles_required('admin')
def update_plan_route(plan_id):
    try:
        data = request.get_json()
        plan_data = UpdatePlanSchema(**data)
        updated = update_plan(plan_id, plan_data)
        return jsonify(PlanResponseSchema.from_orm(updated).dict()), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@plans_bp.delete("/<int:plan_id>")
@token_required
@roles_required('admin')
def delete_plan_route(plan_id):
    try:
        delete_plan(plan_id)
        return jsonify({"message": "Plan deleted"}), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
