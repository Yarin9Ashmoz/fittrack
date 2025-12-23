import configparser
from sqlalchemy import create_engine, MetaData, text

DB_NAME = "fittrack"

def get_db_config():
    """
    Reads MySQL connection details from config.ini
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }

def get_server_engine():
    db = get_db_config()
    server_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}"
    engine = create_engine(server_url, echo=True, future=True)
    return engine

def create_database_if_not_exists():
    server_engine = get_server_engine()
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"Database '{DB_NAME}' created (or already exists).")

def get_engine():
    create_database_if_not_exists()
    db = get_db_config()
    db_url = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{DB_NAME}"
    engine = create_engine(db_url, echo=True, future=True)
    return engine

metadata = MetaData()

engine = get_engine()

def create_all_tables():
    metadata.create_all(engine)
    print("All tables in metadata were created (if not existing).")

def get_connection():
    return engine.connect()

if __name__ == "__main__":
    with get_connection() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.scalar_one()
        print(f"Connected to database: {db_name}")
