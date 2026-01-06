from flask import Blueprint, request, jsonify
from sqlalchemy import select, or_
from backend.app.db.database import engine
from backend.app.models.user import users
from backend.app.models.plan import plans
from backend.app.models.class_session import class_sessions

search_bp = Blueprint("search", __name__)

@search_bp.get("/search")
def search_route():
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"results": []}), 200

    results = []

    with engine.connect() as conn:

        user_query = (
            select(users)
            .where(
                or_(
                    users.c.first_name.ilike(f"%{query}%"),
                    users.c.last_name.ilike(f"%{query}%"),
                    users.c.email.ilike(f"%{query}%"),
                    users.c.phone.ilike(f"%{query}%"),
                )
            )
        )
        user_rows = conn.execute(user_query).fetchall()

        for u in user_rows:
            results.append({
                "id": u.id,
                "type": "user",
                "name": f"{u.first_name} {u.last_name}",
                "email": u.email,
                "phone": u.phone,
            })

        class_query = (
            select(class_sessions)
            .where(class_sessions.c.title.ilike(f"%{query}%"))
        )
        class_rows = conn.execute(class_query).fetchall()

        for c in class_rows:
            results.append({
                "id": c.id,
                "type": "class",
                "class_name": c.title,
            })

        plan_query = (
            select(plans)
            .where(plans.c.name.ilike(f"%{query}%"))
        )
        plan_rows = conn.execute(plan_query).fetchall()

        for p in plan_rows:
            results.append({
                "id": p.id,
                "type": "plan",
                "plan_name": p.name,
            })

    return jsonify({"results": results}), 200
