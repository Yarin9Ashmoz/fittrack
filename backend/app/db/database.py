import configparser
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

DB_NAME = "fittrack"

Base = declarative_base()
metadata = Base.metadata

def get_db_config():
    import os
    config = configparser.ConfigParser()
    # Get path relative to this file
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
    return create_engine(server_url, echo=True, future=True)

def create_database_if_not_exists():
    engine = get_server_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"Database '{DB_NAME}' created (or already exists).")

def get_engine():
    create_database_if_not_exists()
    db = get_db_config()
    db_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{DB_NAME}"
    return create_engine(db_url, echo=True, future=True)

engine = get_engine()

# Imports moved to create_all_tables to avoid circular dependency

def create_all_tables(drop_first=False):
    # Import models here to ensure they are registered with metadata
    from backend.app.models import (
        user,
        workout_plan,
        workout_item,
        subscription,
        payment,
        enrollment,
        checkin,
        class_session,
        plan,
        exercise,
    )
    if drop_first:
        print("Dropping all tables...")
        Base.metadata.drop_all(engine)
    
    Base.metadata.create_all(engine)
    print("All tables created.")

def get_connection():
    return engine.connect()

if __name__ == "__main__":
    create_all_tables()
    print("Connected successfully.")
