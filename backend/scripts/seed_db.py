"""
Seed database with sample data for development and testing.
Uses dynamic ID fetching to ensure foreign key constraints are met.
"""

from datetime import date, timedelta, datetime
from sqlalchemy import text
from backend.app.db.database import engine
from backend.app.models.user import users
from backend.app.models.plan import plans
from backend.app.models.subscription import subscriptions
from backend.app.models.class_session import class_sessions
from backend.app.models.enrollment import enrollments
from backend.app.models.checkin import checkins
from backend.app.models.payment import payments
from backend.app.models.workout_plan import workout_plans
from backend.app.models.workout_item import workout_items


def clear_all_tables():
    """Clear all existing data from tables and reset auto-increment."""
    print("🧹 Clearing existing data and resetting IDs...")
    tables = [
        "checkins", "workout_items", "workout_plans", "payments", 
        "enrollments", "class_sessions", "subscriptions", "plans", "users", "exercise"
    ]
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in tables:
            try:
                conn.execute(text(f"TRUNCATE TABLE {table};"))
            except Exception as e:
                print(f"⚠️ Could not truncate {table}: {e}")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        conn.commit()
    print("✅ All tables cleared and IDs reset")


def seed_users():
    """Seed users table and return a mapping of email to ID."""
    print("👥 Seeding users...")
    sample_users = [
        {"first_name": "יוסי", "last_name": "כהן", "email": "yossi@example.com", "phone": "050-1234567", "role": "admin", "status": "active"},
        {"first_name": "שרה", "last_name": "לוי", "email": "sara@example.com", "phone": "052-2345678", "role": "trainer", "status": "active"},
        {"first_name": "דוד", "last_name": "ישראלי", "email": "david@example.com", "phone": "053-3456789", "role": "trainer", "status": "active"},
        {"first_name": "מיכל", "last_name": "אברהם", "email": "michal@example.com", "phone": "054-4567890", "role": "member", "status": "active"},
        {"first_name": "רון", "last_name": "מזרחי", "email": "ron@example.com", "phone": "055-5678901", "role": "member", "status": "active"},
        {"first_name": "נועה", "last_name": "כהן", "email": "noa@example.com", "phone": "050-6789012", "role": "member", "status": "active"},
        {"first_name": "אלי", "last_name": "שמש", "email": "eli@example.com", "phone": "052-7890123", "role": "member", "status": "active"},
    ]
    
    user_ids = {}
    with engine.connect() as conn:
        for user_data in sample_users:
            result = conn.execute(users.insert().values(**user_data))
            user_ids[user_data["email"]] = result.inserted_primary_key[0]
        conn.commit()
    print(f"✅ Created {len(sample_users)} users")
    return user_ids


def seed_plans():
    """Seed plans table and return a mapping of name to ID."""
    print("📋 Seeding plans...")
    sample_plans = [
        {"name": "Basic Monthly", "type": "monthly", "price": 299.0, "valid_days": 30, "max_entries": 12},
        {"name": "Premium Monthly", "type": "monthly", "price": 499.0, "valid_days": 30, "max_entries": None},
        {"name": "Punch Card 10", "type": "punch_card", "price": 350.0, "valid_days": 90, "max_entries": 10},
        {"name": "Yearly", "type": "yearly", "price": 3000.0, "valid_days": 365, "max_entries": None},
    ]
    
    plan_ids = {}
    with engine.connect() as conn:
        for plan_data in sample_plans:
            result = conn.execute(plans.insert().values(**plan_data))
            plan_ids[plan_data["name"]] = result.inserted_primary_key[0]
        conn.commit()
    print(f"✅ Created {len(sample_plans)} plans")
    return plan_ids


def seed_subscriptions(user_ids, plan_ids):
    """Seed subscriptions table."""
    print("💳 Seeding subscriptions...")
    today = date.today()
    
    sub_data = [
        {"user_id": user_ids["michal@example.com"], "plan_id": plan_ids["Premium Monthly"], "status": "active", "start_date": today - timedelta(days=10), "end_date": today + timedelta(days=20), "remaining_entries": None, "frozen_until": None},
        {"user_id": user_ids["ron@example.com"], "plan_id": plan_ids["Basic Monthly"], "status": "active", "start_date": today - timedelta(days=5), "end_date": today + timedelta(days=25), "remaining_entries": 8, "frozen_until": None},
        {"user_id": user_ids["noa@example.com"], "plan_id": plan_ids["Punch Card 10"], "status": "active", "start_date": today - timedelta(days=15), "end_date": today + timedelta(days=75), "remaining_entries": 7, "frozen_until": None},
        {"user_id": user_ids["eli@example.com"], "plan_id": plan_ids["Basic Monthly"], "status": "expired", "start_date": today - timedelta(days=60), "end_date": today - timedelta(days=30), "remaining_entries": 0, "frozen_until": None},
    ]
    
    sub_ids = []
    with engine.connect() as conn:
        for data in sub_data:
            result = conn.execute(subscriptions.insert().values(**data))
            sub_ids.append(result.inserted_primary_key[0])
        conn.commit()
    print(f"✅ Created {len(sub_ids)} subscriptions")
    return sub_ids


def seed_classes(user_ids):
    """Seed class sessions."""
    print("🏋️ Seeding class sessions...")
    today = date.today()
    
    class_data = [
        {"title": "Morning Yoga", "starts_at": datetime.combine(today + timedelta(days=1), datetime.min.time().replace(hour=7)), "capacity": 15, "trainer_id": user_ids["sara@example.com"], "status": "scheduled"},
        {"title": "CrossFit", "starts_at": datetime.combine(today + timedelta(days=1), datetime.min.time().replace(hour=18)), "capacity": 20, "trainer_id": user_ids["david@example.com"], "status": "scheduled"},
        {"title": "Pilates", "starts_at": datetime.combine(today + timedelta(days=2), datetime.min.time().replace(hour=9)), "capacity": 12, "trainer_id": user_ids["sara@example.com"], "status": "scheduled"},
        {"title": "Strength Training", "starts_at": datetime.combine(today + timedelta(days=2), datetime.min.time().replace(hour=19)), "capacity": 15, "trainer_id": user_ids["david@example.com"], "status": "scheduled"},
    ]
    
    class_ids = []
    with engine.connect() as conn:
        for data in class_data:
            result = conn.execute(class_sessions.insert().values(**data))
            class_ids.append(result.inserted_primary_key[0])
        conn.commit()
    print(f"✅ Created {len(class_ids)} class sessions")
    return class_ids


def seed_enrollments(user_ids, class_ids):
    """Seed enrollments."""
    print("📝 Seeding enrollments...")
    
    enroll_data = [
        {"member_id": user_ids["michal@example.com"], "class_id": class_ids[0], "status": "active"},
        {"member_id": user_ids["ron@example.com"], "class_id": class_ids[0], "status": "active"},
        {"member_id": user_ids["noa@example.com"], "class_id": class_ids[1], "status": "active"},
        {"member_id": user_ids["michal@example.com"], "class_id": class_ids[2], "status": "active"},
        {"member_id": user_ids["ron@example.com"], "class_id": class_ids[3], "status": "active"},
    ]
    
    with engine.connect() as conn:
        conn.execute(enrollments.insert(), enroll_data)
        conn.commit()
    print(f"✅ Created {len(enroll_data)} enrollments")


def seed_checkins(user_ids, sub_ids):
    """Seed check-ins."""
    print("✅ Seeding check-ins...")
    today = date.today()
    
    check_data = [
        {"member_id": user_ids["michal@example.com"], "subscription_id": sub_ids[0], "class_id": None, "timestamp": datetime.combine(today - timedelta(days=5), datetime.min.time().replace(hour=10))},
        {"member_id": user_ids["ron@example.com"], "subscription_id": sub_ids[1], "class_id": None, "timestamp": datetime.combine(today - timedelta(days=3), datetime.min.time().replace(hour=18))},
        {"member_id": user_ids["noa@example.com"], "subscription_id": sub_ids[2], "class_id": None, "timestamp": datetime.combine(today - timedelta(days=2), datetime.min.time().replace(hour=7))},
    ]
    
    with engine.connect() as conn:
        conn.execute(checkins.insert(), check_data)
        conn.commit()
    print(f"✅ Created {len(check_data)} check-ins")


def seed_payments(sub_ids):
    """Seed payments."""
    print("💰 Seeding payments...")
    today = date.today()
    
    pay_data = [
        {"subscription_id": sub_ids[0], "amount": 499.0, "status": "completed", "paid_at": today - timedelta(days=10), "reference": "PAY-001"},
        {"subscription_id": sub_ids[1], "amount": 299.0, "status": "completed", "paid_at": today - timedelta(days=5), "reference": "PAY-002"},
        {"subscription_id": sub_ids[2], "amount": 350.0, "status": "completed", "paid_at": today - timedelta(days=15), "reference": "PAY-003"},
    ]
    
    with engine.connect() as conn:
        conn.execute(payments.insert(), pay_data)
        conn.commit()
    print(f"✅ Created {len(pay_data)} payments")


def seed_workout_plans(user_ids):
    """Seed workout plans."""
    print("💪 Seeding workout plans...")
    today = date.today()
    
    wp_data = [
        {"member_id": user_ids["michal@example.com"], "trainer_id": user_ids["david@example.com"], "title": "Beginner Strength", "created_at": today - timedelta(days=7), "is_active": True},
        {"member_id": user_ids["ron@example.com"], "trainer_id": user_ids["sara@example.com"], "title": "Cardio & Flexibility", "created_at": today - timedelta(days=5), "is_active": True},
    ]
    
    wp_ids = []
    with engine.connect() as conn:
        for data in wp_data:
            result = conn.execute(workout_plans.insert().values(**data))
            wp_ids.append(result.inserted_primary_key[0])
        conn.commit()
    print(f"✅ Created {len(wp_ids)} workout plans")
    return wp_ids


def seed_workout_items(wp_ids):
    """Seed workout items."""
    print("🏃 Seeding workout items...")
    
    wi_data = [
        {"plan_id": wp_ids[0], "exercise_name": "Squats", "sets": 3, "reps": 12, "target_weight": 20.0, "notes": "Focus on form"},
        {"plan_id": wp_ids[0], "exercise_name": "Push-ups", "sets": 3, "reps": 10, "target_weight": None, "notes": "On knees if needed"},
        {"plan_id": wp_ids[1], "exercise_name": "Treadmill", "sets": 1, "reps": 20, "target_weight": None, "notes": "Medium pace 20 min"},
    ]
    
    with engine.connect() as conn:
        conn.execute(workout_items.insert(), wi_data)
        conn.commit()
    print(f"✅ Created {len(wi_data)} workout items")


def main():
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    clear_all_tables()
    
    u_ids = seed_users()
    p_ids = seed_plans()
    s_ids = seed_subscriptions(u_ids, p_ids)
    c_ids = seed_classes(u_ids)
    
    seed_enrollments(u_ids, c_ids)
    seed_checkins(u_ids, s_ids)
    seed_payments(s_ids)
    w_ids = seed_workout_plans(u_ids)
    seed_workout_items(w_ids)
    
    print("=" * 50)
    print("🎉 Database seeding completed successfully!")


if __name__ == "__main__":
    main()
