# Mejores prácticas y recomendaciones

Este documento resume buenas prácticas que conviene aplicar a este proyecto para que se vea más profesional y sea más fácil de mantener.

## 1. Mantener separación de responsabilidades

Cada capa debe tener un propósito claro:

- routers: recibir peticiones
- services: lógica de negocio
- repositories: acceso a datos
- schemas: validación y serialización de datos

Esto evita que el código crezca desordenado.

## 2. Usar DTOs para definir la forma de los datos

Los DTOs ayudan a:

- validar entradas
- controlar qué datos salen al cliente
- evitar exponer campos sensibles como la contraseña

## 3. No guardar secretos en el código

Las claves JWT, tokens y configuraciones sensibles deben ir en variables de entorno.

## 4. Hashear contraseñas siempre

Nunca guardar contraseñas en texto plano. En este proyecto se usa bcrypt, que es una buena práctica.

## 5. Centralizar el manejo de errores

En lugar de lanzar errores dispersos por todo el código, conviene usar excepciones personalizadas y manejarlas en un solo lugar.

## 6. Documentar los endpoints

FastAPI permite documentar automáticamente la API. Eso mejora mucho la experiencia de desarrollo y facilita la prueba manual.

## 7. Mantener logs útiles

Los logs sirven para depurar y observar el comportamiento del sistema. Es importante registrar eventos importantes, como:

- login fallido
- usuario creado
- error de transacción
- token inválido

## 8. Usar transacciones cuando sea necesario

Cuando una operación cambia varios datos, conviene encapsularla en una transacción para asegurar consistencia.

## 9. Preparar el proyecto para escalar

A medida que crezca, conviene pensar en:

- paginación
- migraciones de base de datos
- tests automatizados
- manejo de roles y permisos
- contenedores y despliegue

## 10. Mantener el código legible

Un código claro es más valioso que un código complejo. Prioriza:

- nombres descriptivos
- funciones pequeñas
- lógica sencilla
- comentarios útiles pero no excesivos

## Qué mejorar en este proyecto específicamente

- agregar tests automatizados
- añadir README más detallado para onboarding
- documentar cada endpoint con ejemplos de request/response
- separar mejor la configuración del entorno
- preparar un flujo de CI/CD
- considerar migraciones con Alembic
