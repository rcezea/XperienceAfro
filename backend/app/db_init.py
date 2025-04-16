from backend.app.database import Base
from backend.app.database import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

# Create tables in the database
Base.metadata.create_all(bind=engine)
