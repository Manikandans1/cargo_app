
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Updated database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://Embassy:Embassy1@localhost/cargoapp"

# Create the PostgreSQL engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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




















# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# SQLALCHAMY_DATABASE_URL = 'sqlite:///./order.db'


# engine = create_engine(SQLALCHAMY_DATABASE_URL,connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()

#     try:
#         yield db
#     finally:
#         db.close()