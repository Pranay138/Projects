# recreate_db.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def recreate_db():
    # Drop existing tables
    models.Base.metadata.drop_all(bind=engine)
    # Create new tables
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    recreate_db()
