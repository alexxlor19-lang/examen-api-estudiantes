# Examen: API de Gestión de Estudiantes

Este proyecto consiste en una **API REST de nivel profesional** desarrollada con **FastAPI** para la gestión integral de estudiantes. Implementa una **arquitectura híbrida de persistencia de datos**, combinando el modelo relacional tradicional con soluciones NoSQL en la nube para logs de eventos, cumpliendo estrictamente con los requerimientos técnicos y consideraciones del examen

---

## Arquitectura del Sistema y Flujo de Datos

El sistema opera bajo un flujo híbrido diseñado para garantizar alta disponibilidad, rendimiento y trazabilidad:

1. **Principal (Relacional):** Toda la gestión transaccional (Altas, Bajas, Modificaciones y Lecturas) se realiza sobre una base de datos local **SQLite** mediante el ORM SQLAlchemy
2. **Auditoría y Telemetría (NoSQL en la Nube):** Cada operación de escritura (`POST`, `PATCH`, `DELETE`) ejecuta una **tarea asíncrona en segundo plano (Background Task)** que registra un documento histórico flexible dentro de un clúster web en **MongoDB Atlas**
3. [cite_start]**Capa de Presentación Dinámica:** Se expone un endpoint optimizado para **HTMX** que renderiza un fragmento HTML parcializado (`partial`), evitando la carga completa de páginas web y optimizando el consumo de ancho de banda

---

## Herramientas Utilizadas

* **Lenguaje:** Python 3.12+
* **Framework Backend:** FastAPI (Validación estricta mediante Pydantic v2) 
* **Base de Datos Relacional:** SQLite (Persistencia local automática)
* **Base de Datos NoSQL:** MongoDB Atlas (Despliegue web en la nube)
* **Conector Asíncrono Mongo:** Motor (AsyncIOMotorClient)
* **Motor de Plantillas:** Jinja2 (Para renderizado de componentes HTMX) 

---

##  Estructura Detallada del Proyecto

examen-api-estudiantes/
│
├── database/
│   ├── connection.py       # Configuración del motor de SQLite y sesiones de BD
│   └── mongodb.py          # Conexión web a MongoDB Atlas y función de logs asíncronos
│
├── models/
│   ├── student_db.py       # Modelo de la tabla 'students' en SQLAlchemy (SQLite)
│   └── student_schema.py   # Esquemas Pydantic para validación de payloads de entrada/salida
│
├── routes/
│   └── student_routes.py   # Lógica analítica y de negocio de los 8 Endpoints del sistema
│
├── templates/
│   └── partials/
│       └── tabla.html      # Plantilla HTML fragmentada (Partial) para inyección HTMX
│
├── .gitignore              # Archivos y carpetas excluidos del control de versiones (Git)
├── main.py                 # Punto de entrada de la aplicación e inicialización de tablas
└── README.md               # Documentación técnica del proyecto (Este archivo)