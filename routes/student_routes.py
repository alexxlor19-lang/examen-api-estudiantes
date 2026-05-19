# routes/student_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from database.connection import get_db
from models.student_db import StudentDB
from models.student_schema import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# 1. Crear un estudiante (POST /students) [cite: 37, 40]
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    # Validar si el DNI ya existe (Debe ser único) [cite: 29, 86]
    db_student = db.query(StudentDB).filter(StudentDB.dni == student_data.dni).first()
    if db_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El DNI ya se encuentra registrado."
        )
    
    # Crear la instancia del modelo de Base de Datos
    new_student = StudentDB(**student_data.model_dump())
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# 2. Obtener todos los estudiantes (GET /students) [cite: 41, 44]
@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).all()

# 7. Promedio de notas (GET /students/average) [cite: 61, 64]
# NOTA: Ponemos esta ruta ANTES de /students/{id} para que FastAPI no confunda la palabra "average" con un ID entero.
@router.get("/average")
def get_students_average(db: Session = Depends(get_db)):
    # Calculamos el promedio directamente usando funciones agregadas SQL para mayor eficiencia
    average = db.query(func.avg(StudentDB.grade)).scalar()
    if average is None:
        return {"average": 0.0, "message": "No hay estudiantes registrados aún."}
    return {"average": round(average, 2)}

# 3. Obtener un estudiante por ID (GET /students/{id}) [cite: 45, 48]
@router.get("/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no fue encontrado." # Manejo de errores [cite: 87]
        )
    return student

# 4. Actualizar un estudiante (PUT/PATCH /students/{id}) [cite: 49, 51]
@router.patch("/{id}", response_model=StudentResponse)
def update_student(id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no existe."
        )
    
    # Extraer solo los campos que el usuario envió para actualizar (ignora los campos None)
    update_fields = student_data.model_dump(exclude_unset=True)
    
    # Validar si intenta cambiar a un DNI que ya pertenece a OTRO estudiante
    if "dni" in update_fields:
        dni_check = db.query(StudentDB).filter(StudentDB.dni == update_fields["dni"], StudentDB.id != id).first()
        if dni_check:
            raise HTTPException(status_code=400, detail="El DNI ya está en uso por otro estudiante.")

    for key, value in update_fields.items():
        setattr(student, key, value)
        
    # El requerimiento exige actualizar forzosamente la fecha de modificación [cite: 52, 87]
    student.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(student)
    return student

# 5. Eliminar un estudiante (DELETE /students/{id}) [cite: 53, 56]
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no existe."
        )
    db.delete(student)
    db.commit()
    return {"message": f"Estudiante con ID {id} eliminado correctamente."}

# 6. Creación masiva (Bulk insert) (POST /students/bulk) [cite: 57, 60]
@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def bulk_insert_students(students_list: List[StudentCreate], db: Session = Depends(get_db)):
    inserted_count = 0
    errors = []
    
    for index, student_data in enumerate(students_list):
        # Validar DNI duplicado internamente en la BD
        dni_exists = db.query(StudentDB).filter(StudentDB.dni == student_data.dni).first()
        if dni_exists:
            errors.append(f"Fila {index}: El DNI {student_data.dni} ya existe.")
            continue
            
        new_student = StudentDB(**student_data.model_dump())
        db.add(new_student)
        inserted_count += 1
        
    if inserted_count > 0:
        db.commit()
        
    return {
        "message": f"Inserción masiva completada exitosamente.",
        "registros_insertados": inserted_count,
        "errores": errors
    }