# Evidencia A1 - Contrato de consulta REST SmartDoor

## Proyecto
SmartDoor - Sistema IoT de monitoreo de puertas.

## Objetivo
Diseñar los recursos y endpoints REST para consultar
dispositivos y mediciones almacenadas en SQLite.

## Matriz de diseño

| Pregunta | Respuesta del equipo |
|---|---|
| ¿Qué recursos expondrá la API? | devices y measurements |
| ¿Qué endpoint devuelve todos los dispositivos? | GET /api/devices |
| ¿Qué endpoint devuelve un dispositivo específico? | GET /api/devices/{device_id} |
| ¿Cómo se filtrarán mediciones por device_id? | GET /api/measurements?device_id=DOOR-001 |
| ¿Qué respuesta se espera si el dispositivo no existe? | HTTP 404 Not Found con mensaje JSON |
| ¿Qué límite máximo de registros permitirá la API? | 100 registros por consulta |

## Endpoints propuestos

| Método | Endpoint | Funcionalidad |
|---|---|---|
| GET | /api/devices | Listar dispositivos |
| GET | /api/devices/{device_id} | Consultar dispositivo específico |
| GET | /api/measurements | Consultar mediciones |
| GET | /api/measurements?device_id=DOOR-001 | Filtrar mediciones por dispositivo |
| GET | /api/measurements?limit=20&offset=0 | Paginar resultados |

## Justificación

La API REST de SmartDoor permitirá consultar los
dispositivos y las mediciones registradas en SQLite.
Los endpoints GET facilitarán la recuperación de
información sin modificar los registros existentes.
El parámetro device_id permitirá filtrar las lecturas
de cada sensor de puerta. La paginación mediante
limit y offset permitirá controlar la cantidad de
información devuelta, estableciendo un máximo de
100 registros por solicitud. Cuando un dispositivo
no exista, la API responderá con HTTP 404.
Este diseño permitirá ampliar el backend FastAPI
existente sin reconstruir el proyecto.

## Estado

Diseño propuesto para implementar en la Guía 4.
