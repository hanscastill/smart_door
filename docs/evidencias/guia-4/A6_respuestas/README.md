# Evidencia A6 - Respuestas, errores y Swagger/OpenAPI

## Proyecto SmartDoor

Guía 4 - Fase 6

## 1. Objetivo

Verificar que la API REST SmartDoor responda correctamente
a consultas válidas e inválidas, utilizando códigos HTTP
y documentación interactiva Swagger/OpenAPI.

## 2. Herramientas utilizadas

- Python
- FastAPI
- Uvicorn
- SQLite
- GitHub Codespaces
- Swagger UI
- curl

## 3. Actividades realizadas

Se ejecutaron siete pruebas manuales:

1. Consulta de mediciones existentes.
2. Consulta filtrada por dispositivo DOOR-001.
3. Consulta sin coincidencias para DOOR-999.
4. Listado de dispositivos.
5. Consulta del dispositivo DOOR-001.
6. Consulta de dispositivo inexistente DOOR-999.
7. Validación de límite inválido igual a 500.

## 4. Resultados

Las siete pruebas obtuvieron los códigos esperados.

- HTTP 200: consulta correcta.
- HTTP 200 con lista vacía: sin coincidencias.
- HTTP 404: dispositivo inexistente.
- HTTP 422: parámetro fuera del rango permitido.

## 5. Verificación Swagger/OpenAPI

Se accedió a la documentación interactiva mediante:

http://127.0.0.1:8000/docs

Se verificaron los parámetros:

- device_id
- limit
- offset
- from
- to

También se ejecutó una consulta histórica desde Swagger
para el dispositivo DOOR-001.

La API respondió HTTP 200 y devolvió cinco mediciones.

## 6. Evidencias

- A6_01_swagger_endpoints.png
- A6_02_swagger_consulta_200.png
- matriz_pruebas_A6.md

## 7. Conclusión

La API REST SmartDoor demuestra un comportamiento
correcto ante solicitudes válidas e inválidas.

Los códigos HTTP permiten distinguir entre consultas
exitosas, resultados vacíos, dispositivos inexistentes
y parámetros incorrectos.

Swagger/OpenAPI facilita la documentación, exploración
y prueba de los endpoints disponibles.
