from backend.app.db.database import SessionLocal
from backend.app.models.user import User
from backend.app.models.plan import Plan
from backend.app.models.exercise import Exercise
import bcrypt

def seed_data():
    session = SessionLocal()
    
    # 1. Create Admin User
    existing_admin = session.query(User).filter_by(email="admin@example.com").first()
    if not existing_admin:
        hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            phone="1234567890",
            role="admin",
            status="active",
            national_id="000000000",
            password_hash=hashed_password,
            address="Gym HQ"
        )
        session.add(admin)
        print("✅ Admin user created: admin@example.com / password123")
    else:
        print("ℹ️ Admin user already exists")

    # 2. Create Basic Plans
    if session.query(Plan).count() == 0:
        session.add(Plan(name="Monthly Membership", type="monthly", price=50.0, valid_days=30))
        session.add(Plan(name="10 Entry Pass", type="entries", price=120.0, max_entries=10, valid_days=90))
        print("✅ Basic plans created")

    session.commit()
    session.close()

if __name__ == "__main__":
    seed_data()
