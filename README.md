# FastAPI JWT CRUD API

Esta API muestra un ejemplo práctico de un backend en Python con FastAPI, autenticación JWT, manejo de usuarios y una arquitectura limpia basada en capas.

## ¿Qué hace este proyecto?

- Registra y gestiona usuarios.
- Permite autenticación mediante email y contraseña.
- Emite y valida tokens JWT.
- Usa dependencias para proteger rutas.
- Se apoya en SQLAlchemy para acceso a base de datos.
- Usa Pydantic para validar datos de entrada y salida.

## Tecnologías usadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- JWT con python-jose
- bcrypt para contraseñas
- SQLite como base de datos por defecto

## Estructura del proyecto

```text
api/
  config/
  dependencies/
  entities/
  exceptions/
  mappers/
  middlewares/
  repositories/
  routers/
  schemas/
  security/
  services/
main.py
```

## Requisitos

- Python 3.12 o superior
- Entorno virtual activado

## Instalación

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

1. Crear un archivo .env basado en .env.example:

```powershell
Copy-Item .env.example .env
```

1. Ejecutar la aplicación:

```powershell
uvicorn main:app --reload
```

La API quedará disponible en:

- <http://127.0.0.1:8000/docs>
- <http://127.0.0.1:8000/redoc>

## Variables de entorno

El proyecto espera estas variables:

```env
JWT_SECRET_KEY=tu_clave_secreta
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=60
DATABASE_URI=sqlite:///./db.sqlite
BCRYPT_ROUNDS=12
```

## Endpoints principales

### Autenticación

- POST /oauth/token: login con JSON
- POST /oauth/token/form: login con formulario OAuth2

### Usuarios

- GET /users/: lista usuarios
- GET /users/{id}: obtiene un usuario por id
- POST /users/: crea un usuario
- PUT /users/{id}: actualiza un usuario
- DELETE /users/{id}: elimina un usuario

## Flujo de autenticación

1. El cliente envía email y contraseña.
2. El servicio valida credenciales.
3. Si son correctas, se genera un token JWT.
4. El token se usa para acceder a rutas protegidas.

## Notas de aprendizaje

Este proyecto es ideal para estudiar:

- Arquitectura por capas
- Dependencias en FastAPI
- DTOs con Pydantic
- Repositorios y servicios
- JWT y seguridad básica
- Manejo de errores personalizados

## Próximos pasos recomendados

- Añadir tests automatizados
- Agregar paginación
- Implementar refresh tokens
- Añadir migraciones con Alembic
- Mejorar el manejo de roles y permisos
- Preparar Docker para despliegue

- [x] Arquitectura en capas (Routers, Services, Repositories)
- [x] Autenticación JWT y Hashing
- [x] Logging estructurado en JSON y Request ID
- [ ] Tests unitarios y de integración con `pytest` (En proceso)
- [ ] Dockerización de la aplicación (En proceso)
