from sqlalchemy import Column, Integer, Date, Time, Boolean, ForeignKey, UniqueConstraint, Index
from app.config.database import Base

class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"
    __table_args__ = (UniqueConstraint('doctor_id', 'date', 'time', name='unique_doctor_schedule'),
                      Index('idx_doctor_schedule', 'doctor_id', 'date', 'time'))

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True) 
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)