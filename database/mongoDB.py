# database/mongodb.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Definimos la UR local por defecto de MongoDB
MONGO_URL = "mongodb://localhost:27017"

# Inicializamos el cliente asíncrono de Motor
client = AsyncIOMotorClient(MONGO_URL)

# Creamos o apuntamos a la base de datos de logs
db_mongo = client["examen_logs_db"]

# Apuntamos a la colección específica donde caerán
logs_collection = db_mongo["student_audit_logs"]

# Función  asíncrona para guardar un log en segundo plano
async def save_audit_log(action: str, student_id: int, details: dict):
    """
    Registra un evento de auditoría en la colección NoSQL de MongoDB.
    """
    log_document = {
        "action": action,                     # 'CREATE', 'UPDATE' o 'DELETE'
        "student_id": student_id,             # ID del estudiante afectado
        "timestamp": datetime.utcnow(),       # Cuándo ocurrió el evento
        "details": details                    # Datos adicionales guardados de forma flexible
    }
    try:
        await logs_collection.insert_one(log_document)
        print(f"[MongoDB Log] Evento '{action}' registrado exitosamente para el ID {student_id}.")
    except Exception as e:
        print(f"[MongoDB Error] No se pudo guardar el log de auditoría: {e}")