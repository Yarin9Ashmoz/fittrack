"""
Seed database with sample data for development and testing.
Uses SQLAlchemy ORM and session management.
"""

from datetime import date, timedelta, datetime
from sqlalchemy import text
from backend.app.db.database import SessionLocal, engine
from backend.app.models.user import User
from backend.app.models.plan import Plan
from backend.app.models.subscription import Subscription
from backend.app.models.class_session import ClassSession
from backend.app.models.enrollment import Enrollment
from backend.app.models.checkin import Checkin
from backend.app.models.payment import Payment
from backend.app.models.workout_plan import WorkoutPlan
from backend.app.models.workout_item import WorkoutItem
import bcrypt

def clear_all_tables():
    """Clear all existing data from tables and reset auto-increment."""
    print("🧹 Clearing existing data and resetting IDs...")
    tables = [
        "checkins", "workout_items", "workout_plans", "payments", 
        "enrollments", "class_sessions", "subscriptions", "plans", "users"
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


def seed_users(session):
    """Seed users table."""
    print("👥 Seeding users...")
    
    # helper for hashing
    def hash_pw(pw):
        return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    sample_users = [
        User(first_name="יוסי", last_name="כהן", email="yossi@example.com", phone="050-1234567", role="admin", status="active", address="TLV", national_id="100000001", password_hash=hash_pw("password123")),
        User(first_name="שרה", last_name="לוי", email="sara@example.com", phone="052-2345678", role="coach", status="active", address="Haifa", national_id="100000002", password_hash=hash_pw("password123")),
        User(first_name="דוד", last_name="ישראלי", email="david@example.com", phone="053-3456789", role="coach", status="active", address="Jerusalem", national_id="100000003", password_hash=hash_pw("password123")),
        User(first_name="מיכל", last_name="אברהם", email="michal@example.com", phone="054-4567890", role="member", status="active", address="Eilat", national_id="100000004", password_hash=hash_pw("password123")),
        User(first_name="רון", last_name="מזרחי", email="ron@example.com", phone="055-5678901", role="member", status="active", address="Ashdod", national_id="100000005", password_hash=hash_pw("password123")),
        User(first_name="נועה", last_name="כהן", email="noa@example.com", phone="050-6789012", role="member", status="active", address="Holo", national_id="100000006", password_hash=hash_pw("password123")),
        User(first_name="אלי", last_name="שמש", email="eli@example.com", phone="052-7890123", role="member", status="active", address="Bat Yam", national_id="100000007", password_hash=hash_pw("password123")),
        # Add original Admin for consistency
        User(first_name="Admin", last_name="User", email="admin@example.com", phone="1234567890", role="admin", status="active", address="HQ", national_id="000000000", password_hash=hash_pw("password123"))
    ]
    
    session.add_all(sample_users)
    session.commit()
    
    # Reload mapping
    user_map = {u.email: u.id for u in session.query(User).all()}
    print(f"✅ Created {len(sample_users)} users")
    return user_map


def seed_plans(session):
    """Seed plans table."""
    print("📋 Seeding plans...")
    sample_plans = [
        Plan(name="Basic Monthly", type="monthly", price=299.0, valid_days=30, max_entries=12),
        Plan(name="Premium Monthly", type="monthly", price=499.0, valid_days=30, max_entries=None),
        Plan(name="Punch Card 10", type="entries", price=350.0, valid_days=90, max_entries=10),
        Plan(name="Yearly", type="monthly", price=3000.0, valid_days=365, max_entries=None),
    ]
    
    session.add_all(sample_plans)
    session.commit()
    
    plan_map = {p.name: p.id for p in session.query(Plan).all()}
    print(f"✅ Created {len(sample_plans)} plans")
    return plan_map


def seed_subscriptions(session, user_ids, plan_ids):
    """Seed subscriptions table."""
    print("💳 Seeding subscriptions...")
    today = date.today()
    
    subs = [
        Subscription(user_id=user_ids["michal@example.com"], plan_id=plan_ids["Premium Monthly"], status="active", start_date=today - timedelta(days=10), end_date=today + timedelta(days=20), remaining_entries=None, frozen_until=None, debt=0),
        Subscription(user_id=user_ids["ron@example.com"], plan_id=plan_ids["Basic Monthly"], status="active", start_date=today - timedelta(days=5), end_date=today + timedelta(days=25), remaining_entries=8, frozen_until=None, debt=0),
        Subscription(user_id=user_ids["noa@example.com"], plan_id=plan_ids["Punch Card 10"], status="active", start_date=today - timedelta(days=15), end_date=today + timedelta(days=75), remaining_entries=7, frozen_until=None, debt=0),
        Subscription(user_id=user_ids["eli@example.com"], plan_id=plan_ids["Basic Monthly"], status="expired", start_date=today - timedelta(days=60), end_date=today - timedelta(days=30), remaining_entries=0, frozen_until=None, debt=0),
    ]
    
    session.add_all(subs)
    session.commit()
    
    all_subs = session.query(Subscription).all()
    print(f"✅ Created {len(subs)} subscriptions")
    return all_subs


def seed_classes(session, user_ids):
    """Seed class sessions."""
    print("🏋️ Seeding class sessions...")
    today = date.today()
    
    # Corrected fields: starts_at (not start_time), remove duration/minutes if not in model (verified not in model)
    classes = [
        ClassSession(title="Morning Yoga", starts_at=datetime.combine(today + timedelta(days=1), datetime.min.time().replace(hour=7)), capacity=15, trainer_id=user_ids["sara@example.com"], status="scheduled"),
        ClassSession(title="CrossFit", starts_at=datetime.combine(today + timedelta(days=1), datetime.min.time().replace(hour=18)), capacity=20, trainer_id=user_ids["david@example.com"], status="scheduled"),
        ClassSession(title="Pilates", starts_at=datetime.combine(today + timedelta(days=2), datetime.min.time().replace(hour=9)), capacity=12, trainer_id=user_ids["sara@example.com"], status="scheduled"),
        ClassSession(title="Strength Training", starts_at=datetime.combine(today + timedelta(days=2), datetime.min.time().replace(hour=19)), capacity=15, trainer_id=user_ids["david@example.com"], status="scheduled"),
    ]
    
    session.add_all(classes)
    session.commit()
    
    all_classes = session.query(ClassSession).all()
    print(f"✅ Created {len(classes)} class sessions")
    return all_classes


def seed_enrollments(session, user_ids, classes):
    """Seed enrollments."""
    print("📝 Seeding enrollments...")
    
    # Corrected fields: member_id, class_id
    enrolls = [
        Enrollment(member_id=user_ids["michal@example.com"], class_id=classes[0].id, status="active"),
        Enrollment(member_id=user_ids["ron@example.com"], class_id=classes[0].id, status="active"),
        Enrollment(member_id=user_ids["noa@example.com"], class_id=classes[1].id, status="active"),
        Enrollment(member_id=user_ids["michal@example.com"], class_id=classes[2].id, status="active"),
        Enrollment(member_id=user_ids["ron@example.com"], class_id=classes[3].id, status="active"),
    ]
    
    session.add_all(enrolls)
    session.commit()
    print(f"✅ Created {len(enrolls)} enrollments")


def seed_checkins(session, user_ids, subscriptions):
    """Seed check-ins."""
    print("✅ Seeding check-ins...")
    today = date.today()
    
    sub_michal = next(s for s in subscriptions if s.user_id == user_ids["michal@example.com"])
    sub_ron = next(s for s in subscriptions if s.user_id == user_ids["ron@example.com"])
    sub_noa = next(s for s in subscriptions if s.user_id == user_ids["noa@example.com"])

    # Corrected fields: member_id, timestamp
    checks = [
        Checkin(member_id=user_ids["michal@example.com"], subscription_id=sub_michal.id, class_id=None, timestamp=datetime.combine(today - timedelta(days=5), datetime.min.time().replace(hour=10))),
        Checkin(member_id=user_ids["ron@example.com"], subscription_id=sub_ron.id, class_id=None, timestamp=datetime.combine(today - timedelta(days=3), datetime.min.time().replace(hour=18))),
        Checkin(member_id=user_ids["noa@example.com"], subscription_id=sub_noa.id, class_id=None, timestamp=datetime.combine(today - timedelta(days=2), datetime.min.time().replace(hour=7))),
    ]
    
    session.add_all(checks)
    session.commit()
    print(f"✅ Created {len(checks)} check-ins")


def seed_payments(session, subscriptions):
    """Seed payments."""
    print("💰 Seeding payments...")
    today = date.today()
    
    subs_to_pay = subscriptions[:3]
    
    # Corrected fields: reference, paid_at. removed method.
    pays = [
        Payment(subscription_id=subs_to_pay[0].id, amount=499.0, status="completed", paid_at=today - timedelta(days=10), reference="PAY-001"),
        Payment(subscription_id=subs_to_pay[1].id, amount=299.0, status="completed", paid_at=today - timedelta(days=5), reference="PAY-002"),
        Payment(subscription_id=subs_to_pay[2].id, amount=350.0, status="completed", paid_at=today - timedelta(days=15), reference="PAY-003"),
    ]
    
    session.add_all(pays)
    session.commit()
    print(f"✅ Created {len(pays)} payments")


def seed_workout_plans(session, user_ids):
    """Seed workout plans."""
    print("💪 Seeding workout plans...")
    today = date.today()
    
    # Corrected fields: trainer_id, title, created_at, is_active. removed goal.
    wps = [
        WorkoutPlan(member_id=user_ids["michal@example.com"], trainer_id=user_ids["david@example.com"], title="Beginner Strength", created_at=today - timedelta(days=7), is_active=True),
        WorkoutPlan(member_id=user_ids["ron@example.com"], trainer_id=user_ids["sara@example.com"], title="Cardio & Flexibility", created_at=today - timedelta(days=5), is_active=True),
    ]
    
    session.add_all(wps)
    session.commit()
    
    all_wps = session.query(WorkoutPlan).all()
    print(f"✅ Created {len(wps)} workout plans")
    return all_wps


def seed_workout_items(session, wps):
    """Seed workout items."""
    print("🏃 Seeding workout items...")
    
    # Corrected fields: exercise_name, sets, reps, target_weight, notes. removed order, exercise_id.
    items = [
        WorkoutItem(plan_id=wps[0].id, exercise_name="Squats", sets=3, reps=12, target_weight=20.0, notes="Focus on form"),
        WorkoutItem(plan_id=wps[0].id, exercise_name="Push-ups", sets=3, reps=10, target_weight=None, notes="On knees if needed"),
        # For treadmill, use notes as there is no duration field in model? Actually wait, model has no duration. Just notes.
        WorkoutItem(plan_id=wps[1].id, exercise_name="Treadmill", sets=1, reps=1, target_weight=None, notes="20 min medium pace"),
    ]
    
    session.add_all(items)
    session.commit()
    print(f"✅ Created {len(items)} workout items")


def main():
    print("🌱 Starting database seeding (ORM)...")
    print("=" * 50)
    
    clear_all_tables()
    
    session = SessionLocal()
    try:
        u_ids = seed_users(session)
        p_ids = seed_plans(session)
        subs = seed_subscriptions(session, u_ids, p_ids)
        classes = seed_classes(session, u_ids)
        
        seed_enrollments(session, u_ids, classes)
        seed_checkins(session, u_ids, subs)
        seed_payments(session, subs)
        wps = seed_workout_plans(session, u_ids)
        seed_workout_items(session, wps)
        
        print("=" * 50)
        print("🎉 Database seeding completed successfully!")
    except Exception as e:
        session.rollback()
        print(f"❌ Custom Seed Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    main()
