from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base 
import enum 

class AppointmentStatus(enum.Enum):
    booked = "booked"
    completed = "completed"
    cancelled = "cancelled"
    rescheduled = "rescheduled"

class Appointment(Base): 
    __tablename__ = "appointments" 

    id = Column(Integer, primary_key=True, index=True) 
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.booked, nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")