from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configuramos la ruta hacia la carpeta de las plantillas HTML
templates = Jinja2Templates(directory="templates")

# routes/student_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from database.connection import get_db
from database.mongoDB import save_audit_log
from models.student_db import StudentDB
from models.student_schema import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# 1. Crear un estudiante (POST /students)
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.dni == student_data.dni).first()
    if db_student:
        raise HTTPException(status_code=400, detail="El DNI ya se encuentra registrado.")
    
    new_student = StudentDB(**student_data.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    # 📌 Tarea en segundo plano: Registrar en MongoDB la creación de forma asíncrona
    log_details = {"dni": new_student.dni, "name": new_student.name}
    background_tasks.add_task(save_audit_log, "CREATE", new_student.id, log_details)
    
    return new_student

# 2. Obtener todos los estudiantes (GET /students)
@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).all()

# 3. Promedio de notas (GET /students/average)
# NOTA: Ponemos esta ruta ANTES de /students/{id} para que FastAPI no confunda la palabra "average" con un ID entero.
@router.get("/average")
def get_students_average(db: Session = Depends(get_db)):
    # Calculamos el promedio directamente usando funciones agregadas SQL para mayor eficiencia
    average = db.query(func.avg(StudentDB.grade)).scalar()
    if average is None:
        return {"average": 0.0, "message": "No hay estudiantes registrados aún."}
    return {"average": round(average, 2)}

# 4. Obtener un estudiante por ID (GET /students/{id})
@router.get("/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no fue encontrado." # Manejo de errores
        )
    return student

# 5. Actualizar un estudiante (PUT/PATCH /students/{id})
@router.patch("/{id}", response_model=StudentResponse)
def update_student(id: int, student_data: StudentUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {id} no existe.")
    
    update_fields = student_data.model_dump(exclude_unset=True)
    
    for key, value in update_fields.items():
        setattr(student, key, value)
        
    student.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(student)
    
    # 📌 Tarea en segundo plano: Registrar en MongoDB la modificación con los campos alterados
    background_tasks.add_task(save_audit_log, "UPDATE", student.id, update_fields)
    
    return student

# 6. Eliminar un estudiante (DELETE /students/{id})
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_student(id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Estudiante con ID {id} no existe.")
    
    # Conservamos los datos básicos para el registro histórico antes del delete
    log_details = {"dni": student.dni, "name": student.name, "deleted_at_node": "SQLite-Main"}
    
    db.delete(student)
    db.commit()
    
    # 📌 Tarea en segundo plano: Registrar en MongoDB la baja
    background_tasks.add_task(save_audit_log, "DELETE", id, log_details)
    
    return {"message": f"Estudiante con ID {id} eliminado correctamente."}

# 7. Creación masiva (Bulk insert) (POST /students/bulk)
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

# 8. Renderizar tabla HTMX (Fragmento / Partial) (GET /students/table)
@router.get("/table", response_class=HTMLResponse)
def get_students_table_partial(request: Request, db: Session = Depends(get_db)):
    students = db.query(StudentDB).all()
    # Enviamos los datos recolectados de la BD hacia la plantilla HTML parcial
    return templates.TemplateResponse("partials/tabla.html", {"request": request, "students": students})