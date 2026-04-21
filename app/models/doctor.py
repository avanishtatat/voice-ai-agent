from sqlalchemy import Column, Integer, String 
from app.config.database import Base

class Doctor(Base):
    __tablename__ = "doctors" 

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False) 
    specialty = Column(String, nullable=False)