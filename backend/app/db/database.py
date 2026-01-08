import configparser
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

DB_NAME = "fittrack"

Base = declarative_base()

def get_db_config():
    import os
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.ini")
    config.read(config_path)
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }

def get_server_engine():
    db = get_db_config()
    server_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}"
    return create_engine(server_url, echo=False, future=True)

def create_database_if_not_exists():
    engine = get_server_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()

def get_engine():
    create_database_if_not_exists()
    db = get_db_config()
    db_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{DB_NAME}"
    return create_engine(db_url, echo=False, future=True)

engine = get_engine()

from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_all_tables(drop_first=False):
    from backend.app.models.user import User
    from backend.app.models.plan import Plan
    from backend.app.models.subscription import Subscription
    from backend.app.models.class_session import ClassSession
    from backend.app.models.enrollment import Enrollment
    from backend.app.models.payment import Payment
    from backend.app.models.checkin import Checkin
    from backend.app.models.exercise import Exercise
    from backend.app.models.workout_plan import WorkoutPlan
    from backend.app.models.workout_item import WorkoutItem
    
    # New feature models
    from backend.app.models.intake_evaluation import IntakeEvaluation
    from backend.app.models.personal_tracking import PersonalTracking
    from backend.app.models.error_report import ErrorReport
    
    if drop_first:
        Base.metadata.drop_all(engine)
    
    Base.metadata.create_all(engine)
    print("All tables created successfully, including new feature tables.")


def get_connection():
    return engine.connect()

if __name__ == "__main__":
    create_all_tables()
    print("Connected successfully.")
