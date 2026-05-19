# 📚 Examen: API REST de Gestión de Estudiantes

Este proyecto consiste en una **API REST** desarrollada con **FastAPI** para la gestión de datos de estudiantes utilizando **SQLite** a través de SQLAlchemy. Adicionalmente, incluye la capacidad de renderizar fragmentos dinámicos de HTML diseñados para integrarse nativamente con **HTM**.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python
* **Framework Backend:** FastAPI
* **Mapeo de Datos (ORM):** SQLAlchemy
* **Base de Datos:** SQLite (Generada localmente de forma automática)
* **Motor de Plantillas:** Jinja2 (Para fragmentos HTMX)

---

## 📂 Estructura del Proyecto

La arquitectura del proyecto sigue una organización limpia y modular dividida por responsabilidades:

```text
examen-api-estudiantes/
│
├── database/
│   └── connection.py       # Configuración del motor y sesión de SQLite
│
├── models/
│   ├── student_db.py       # Modelo de datos de la tabla en SQLAlchemy
│   └── student_schema.py   # Esquemas de validación de datos con Pydantic
│
├── routes/
│   └── student_routes.py   # Lógica y definición de los 8 Endpoints de la API
│
├── templates/
│   └── partials/
│       └── tabla.html      # Plantilla del fragmento HTML (Partial) para HTMX
│
├── .gitignore              # Archivos y carpetas excluidos en Git
├── main.py                 # Punto de entrada de la aplicación e inicialización
└── README.md               # Documentación del proyecto