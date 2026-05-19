#student_db.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from database.connection import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String, unique=True, nullable=False, index=True) # Obligatorio y único
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    grade = Column(Float, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False) # No automático
    
    #marcas de tiempo
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)