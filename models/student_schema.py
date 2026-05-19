#student_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Esquema base: se requiere para CREAR un estudiante (POST)
class StudentCreate(BaseModel):
    dni: str = Field(..., min_length=8, max_length=12, description="DNI único del estudiante")
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120) 
    grade: float = Field(..., ge=0.0, le=20.0)
    is_approved: bool = Field(..., description="Estado de aprobación asignado manualmente")

# Esquema para ACTUALIZAR (PUT/PATCH) - Permite campos opcionales
class StudentUpdate(BaseModel):
    dni: Optional[str] = Field(None, min_length=8, max_length=12)
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    grade: Optional[float] = Field(None, ge=0.0, le=20.0)
    is_approved: Optional[bool] = None

# Esquema de RESPUESTA: la API devuelve (incluye ID y timestamps)
class StudentResponse(BaseModel):
    id: int
    dni: str
    name: str
    age: int 
    grade: float
    is_approved: bool 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite mapear objetos de SQLAlchemy a JSON