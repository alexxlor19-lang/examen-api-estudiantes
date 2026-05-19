#student_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Esquema base: se requiere para CREAR un estudiante (POST)
class StudentCreate(BaseModel):
    DNI: str = Field(..., min_length=8, max_length=12, description="DNI único del estudiante")
    NAME: str = Field(..., min_length=2)
    AGE: int = Field(..., ge=0, le=120) 
    GRADE: float = Field(..., ge=0.0, le=20.0)
    is_approved: bool = Field(..., description="Estado de aprobación asignado manualmente")

# Esquema para ACTUALIZAR (PUT/PATCH) - Permite campos opcionales
class StudentUpdate(BaseModel):
    DNI: Optional[str] = Field(None, min_length=8, max_length=12)
    NAME: Optional[str] = None
    AGE: Optional[int] = Field(None, ge=0, le=120)
    GRADE: Optional[float] = Field(None, ge=0.0, le=20.0)
    is_approved: Optional[bool] = None

# Esquema de RESPUESTA: la API devuelve (incluye ID y timestamps)
class StudentResponse(BaseModel):
    ID: int
    DNI: str
    NAME: str
    AGE: int 
    GRADE: float
    is_approved: bool 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite mapear objetos de SQLAlchemy a JSON