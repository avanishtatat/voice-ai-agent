from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey
from app.config.database import Base

class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)