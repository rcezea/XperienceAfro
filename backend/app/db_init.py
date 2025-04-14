# Create a file `init_db.py`:
from sqlalchemy import create_engine
from backend.app.database import Base, DATABASE_URL

engine = create_engine(DATABASE_URL)

# Create tables in the database
Base.metadata.create_all(bind=engine)
