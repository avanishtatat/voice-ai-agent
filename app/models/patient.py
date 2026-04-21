from sqlalchemy import Column, Integer, String
from app.config.database import Base 

class Patient(Base):
    __tablename__ = "patients" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False) 
    preferred_language = Column(String, default="en", nullable=False)
    past_appointments= Column(String) # Store past appointments as a comma-separated string for simplicity