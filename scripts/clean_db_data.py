import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base, Document, Page, Fact

def clean_db_data():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/docufi")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        # Truncate tables in the correct order to avoid foreign key issues
        db.query(Fact).delete()
        db.query(Page).delete()
        db.query(Document).delete()
        db.commit()
        logging.info("Database data cleaned successfully.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error cleaning database data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clean_db_data()
