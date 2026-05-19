# main.py
from fastapi import FastAPI
from database.connection import engine, Base
from routes.student_routes import router as student_router

# Creamos físicamente las tablas en la base de datos SQLite 'students.db' al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Examen API REST Estudiantes",
    description="API REST para la gestión de estudiantes con SQLite e integración HTMX.",
    version="1.0.0"
)

# Incluimos los endpoints modulares que estructuramos en el router
app.include_router(student_router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API REST de Estudiantes",
        "documentation": "/docs" # FastAPI genera la documentación interactiva Swagger aquí de forma nativa
    }