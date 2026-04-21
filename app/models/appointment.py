from sqlalchemy import Column, Integer, Date, Time, ForeignKey, UniqueConstraint, Enum
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
    __table_args__ = (UniqueConstraint('doctor_id', 'date', 'time', name='unique_doctor_appointment'),)

    id = Column(Integer, primary_key=True, index=True) 
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.booked, nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")