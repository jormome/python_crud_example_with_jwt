# Arquitectura del proyecto

Este proyecto sigue un patrón simple pero claro de arquitectura por capas para separar responsabilidades.

## Visión general

La aplicación recibe peticiones a través de los routers, delega la lógica al servicio correspondiente y usa repositorios para interactuar con la base de datos.

## Capa de routers

Los routers se encargan de:

- recibir las peticiones HTTP
- validar el formato de entrada mediante DTOs
- inyectar dependencias
- delegar la lógica a los servicios

Ejemplos:

- [api/routers/auth_router.py](../api/routers/auth_router.py)
- [api/routers/user_router.py](../api/routers/user_router.py)

## Capa de servicios

Los servicios contienen la lógica de negocio.

Responsabilidades:

- validar reglas de negocio
- orquestar operaciones
- manejar transacciones
- transformar entidades a DTOs

Ejemplo principal:

- [api/services/user_service.py](../api/services/user_service.py)

## Capa de repositorios

Los repositorios encapsulan el acceso a datos.

Responsabilidades:

- consultar y modificar registros
- aislar la lógica SQLAlchemy del resto de la app
- dejar la lógica de negocio fuera del acceso a datos

Ejemplo:

- [api/repositories/user_repository.py](../api/repositories/user_repository.py)

## Capa de entidades y schemas

- Las entidades representan los modelos de base de datos.
- Los schemas o DTOs representan la forma de datos que entran y salen de la API.

Ejemplos:

- [api/entities/user.py](../api/entities/user.py)
- [api/schemas/user_dto.py](../api/schemas/user_dto.py)

## Flujo de una petición

```text
Cliente -> Router -> Service -> Repository -> Database
```

### Ejemplo: crear un usuario

1. El router recibe el payload desde POST /users/.
2. El service valida que el email no exista.
3. Se hashea la contraseña.
4. El repositorio guarda el usuario.
5. El service devuelve un DTO de respuesta.

## Seguridad

La seguridad está separada en capas:

- [api/security/passwords_security.py](../api/security/passwords_security.py): hashing de contraseñas con bcrypt
- [api/services/jwt_service.py](../api/services/jwt_service.py): creación y validación de tokens
- [api/dependencies/security_dependency.py](../api/dependencies/security_dependency.py): protección de rutas

## Manejo de errores

Los errores de negocio se encapsulan mediante excepciones personalizadas en [api/exceptions/exceptions.py](../api/exceptions/exceptions.py). Esto ayuda a mantener una respuesta consistente.

## Puntos fuertes de esta arquitectura

- Código más fácil de mantener
- Separación clara de responsabilidades
- Menos acoplamiento entre capas
- Más sencillo de extender

## Mejoras futuras

- añadir migraciones con Alembic
- agregar tests
- introducir paginación
- separar logs y configuración de manera más avanzada
- añadir roles y permisos más robustos
