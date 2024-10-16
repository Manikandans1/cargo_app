
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Updated database URL for PostgreSQL
DATABASE_URL = "postgresql://Embassy:Embassy@12@localhost:5432/cargoapp"

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

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Read environment variables for database connection
# DB_USER = os.getenv("Embassy")        # Set in the DigitalOcean App Platform
# DB_PASSWORD = os.getenv("Embassy1")  # Set in the DigitalOcean App Platform
# DB_HOST = os.getenv("DB_HOST")          # Set in the DigitalOcean App Platform
# DB_PORT = os.getenv("DB_PORT", 5432)    # Default to 5432 if not set
# DB_NAME = os.getenv("cargoapp")          # Set in the DigitalOcean App Platform

# # Updated database URL for PostgreSQL
# SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Create the PostgreSQL engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Session for interacting with the database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for our ORM models
# Base = declarative_base()

# # Dependency for database sessions
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()