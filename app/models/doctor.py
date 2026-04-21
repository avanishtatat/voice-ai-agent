from sqlalchemy import Column, Integer, String 
from sqlalchemy.orm import relationship
from app.config.database import Base

class Doctor(Base):
    __tablename__ = "doctors" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False) 
    specialty = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor") # Establishes a relationship with the Appointment model, allowing access to a doctor's appointments.
    schedules = relationship("DoctorSchedule", back_populates="doctor") # Establishes a relationship with the DoctorSchedule model, allowing access to a doctor's schedules.