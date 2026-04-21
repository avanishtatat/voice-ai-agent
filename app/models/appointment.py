from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from app.config.database import Base 

class Appointment(Base): 
    __tablename__ = "appointments" 

    id = Column(Integer, primary_key=True, index=True) 
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String, default="booked", nullable=False)