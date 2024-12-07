
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Updated database URL for PostgreSQL
DATABASE_URL = "postgresql://Embassy:Embassy12@localhost:5432/cargoapp"

# Create the PostgreSQL engine
engine = create_engine(DATABASE_URL)

# Session for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()