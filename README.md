# Parameter Configuration Service (Microservicio Flask)

Microservicio **CRU** (Create, Read, Update) diseñado para gestionar parámetros de configuración de manera centralizada, utilizando Flask y Flask-SQLAlchemy.

Este servicio resuelve el reto de almacenar y recuperar **valores polimórficos** (distintos tipos de datos) de forma segura en un único campo de texto de base de datos, manteniendo la integridad del tipo original.

## ✨ Características Principales

* **Persistencia:** MySQL (producción), con un diseño de ORM basado en **SQLAlchemy**.
* **Tipos de Datos Soportados:** `String`, `Number` (int/float), `Boolean`, `JSON` (Diccionarios) y `Array` (Listas).
* **Patrón Arquitectónico:** **Application Factory** (`create_app`) para una gestión de configuraciones flexible y escalable.
* **Ready-to-Deploy:** Configurado para entornos `development`, `testing` y `production`.

## 📦 Estructura del Proyecto

```

.
├── parameter\_service/
│   ├── **init**.py         \# Factoría de aplicación (create\_app) e inicialización de SQLAlchemy (db)
│   └── models/
│       └── parameter\_model.py  \# Lógica central del ORM y serialización/deserialización polimórfica
├── app.py                  \# Punto de entrada principal para ejecutar el servidor.
├── config.py               \# Definición de configuraciones por ambiente (Dev, Test, Prod).
└── tests/                  \# Pruebas unitarias con Pytest.

````

## ⚙️ Configuración e Instalación

### 1. Requisitos

* Python 3.10+
* MySQL/MariaDB (para desarrollo/producción)

### 2. Instalación

```bash
# 1. Clonar el repositorio y acceder
# git clone [repo-url]
# cd prueba-tecnica-redeban

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
````

### 3\. Variables de Entorno

El servicio requiere variables de entorno (usualmente definidas en un archivo `.env` local) para la conexión a la base de datos:

| Variable | Ambiente | Propósito | Ejemplo |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | Dev / Prod | URI de conexión a MySQL. | `mysql+pymysql://user:pass@host:3306/db_name` |
| `TEST_DATABASE_URL` | Testing | URI de conexión a SQLite in-memory para tests. | `sqlite:///:memory:` |

## 🚀 Uso y Ejecución

### 1\. Modo Desarrollo

Ejecute el servidor de desarrollo. La inicialización de la app (`app.py`) incluye `db.create_all()` para crear las tablas de MySQL automáticamente (solo en desarrollo).

```bash
source venv/bin/activate
python app.py
# Servidor disponible en [http://0.0.0.0:5000/](http://0.0.0.0:5000/)
```

### 2\. Pruebas Unitarias

Ejecute Pytest para verificar la lógica del modelo y la carga de configuraciones en el ambiente `testing`:

```bash
source venv/bin/activate
pytest
```

## 🌐 Despliegue (Devops)

El diseño modular y el **Application Factory Pattern** permiten un despliegue limpio y parametrizado:

| Ambiente | Configuración | Base de Datos | Debug |
| :--- | :--- | :--- | :--- |
| **Desarrollo** | `DevelopmentConfig` | `DATABASE_URL` (local) | `True` |
| **Pruebas (Tests)** | `TestingConfig` | `TEST_DATABASE_URL` (SQLite in-memory) | `False` |
| **Producción** | `ProductionConfig` | `DATABASE_URL` (cluster) | `False` |

Para despliegues en **AWS ECS** o **Kubernetes**, se recomienda utilizar el comando `flask db migrate` (con Flask-Migrate/Alembic) en lugar de `db.create_all()` para gestionar el esquema de la base de datos de forma segura.
