from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base 

class Patient(Base):
    __tablename__ = "patients" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False) 
    preferred_language = Column(String, default="en", nullable=False)
    
    appointments = relationship("Appointment", back_populates="patient") # Establishes a relationship with the Appointment model, allowing access to a patient's appointments.