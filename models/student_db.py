#student_db.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from database.connection import Base

class StudentDB(Base):
    __tablename__ = "students"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    DNI = Column(String, unique=True, nullable=False, index=True) # Obligatorio y único
    NAME = Column(String, nullable=False) [cite: 30]
    AGE = Column(Integer, nullable=False) [cite: 31]
    GRADE = Column(Float, nullable=False) [cite: 32]
    is_approved = Column(Boolean, default=False, nullable=False) # No automático
    
    #marcas de tiempo
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)