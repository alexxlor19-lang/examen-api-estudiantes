# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definimos el archivo local de SQLite
DATABASE_URL = "sqlite:///./students.db"

# El argumento connect_args es específico para que SQLite permita múltiples hilos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Creamos una fábrica de sesiones para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la cual heredarán nuestros modelos de base de datos
Base = declarative_base()

# Función auxiliar (Dependency Injection) para abrir y cerrar la sesión por cada petición HTTP
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()