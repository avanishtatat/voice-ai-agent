import os
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
from typing import Generator
from sqlalchemy.orm import Session

# Load environment variables from .env file
load_dotenv() 

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL: 
    raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session and ensures cleanup after use."""
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close()

# Create a base class for declarative class definitions
Base = declarative_base()