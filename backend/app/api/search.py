from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from backend.app.db.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.plan import Plan
from backend.app.models.class_session import ClassSession

search_bp = Blueprint("search", __name__)

@search_bp.get("/search")
def search_route():
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"results": []}), 200

    results = []

    with SessionLocal() as session:
        # User Search
        user_rows = session.query(User).filter(
            or_(
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
                User.phone.ilike(f"%{query}%")
            )
        ).all()

        for u in user_rows:
            results.append({
                "id": u.id,
                "type": "user",
                "name": f"{u.first_name} {u.last_name}",
                "email": u.email,
                "phone": u.phone,
            })

        # Class Search
        class_rows = session.query(ClassSession).filter(
            ClassSession.title.ilike(f"%{query}%")
        ).all()

        for c in class_rows:
            results.append({
                "id": c.id,
                "type": "class",
                "class_name": c.title,
            })

        # Plan Search
        plan_rows = session.query(Plan).filter(
            Plan.name.ilike(f"%{query}%")
        ).all()

        for p in plan_rows:
            results.append({
                "id": p.id,
                "type": "plan",
                "plan_name": p.name,
            })

    return jsonify({"results": results}), 200
