"""Compatibility entry point for database initialization."""

from models.database import DB_PATH, initialize_database


if __name__ == "__main__":
    initialize_database()
    print(f"Initialized {DB_PATH}")
