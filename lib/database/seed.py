from .connection import get_connection

def seed_database():
    with get_connection() as conn:
        # Add seed data here
        pass