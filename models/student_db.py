# models/student_db.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from database.connection import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String, unique=True, nullable=False, index=True) # Obligatorio y único [cite: 29]
    name = Column(String, nullable=False) [cite: 30]
    age = Column(Integer, nullable=False) [cite: 31]
    grade = Column(Float, nullable=False) [cite: 32]
    is_approved = Column(Boolean, default=False, nullable=False) # No automático [cite: 33]
    
    # Manejo automático de marcas de tiempo [cite: 34, 35]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)