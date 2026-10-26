# Fase 8 - Pruebas automatizadas de la API SmartDoor

## 1. Propósito

Convertir las verificaciones principales de la API REST
SmartDoor en pruebas automatizadas, repetibles y capaces
de detectar regresiones.

## 2. Herramientas utilizadas

- Python 3.12
- FastAPI
- Pytest
- TestClient
- SQLite
- GitHub Codespaces

## 3. Implementación

Se creó el archivo:

tests/test_api_queries.py

Este archivo contiene cinco pruebas automatizadas.

Se utiliza una base de datos SQLite temporal para
evitar modificar los registros originales de SmartDoor.

## 4. Pruebas realizadas

| Prueba | Resultado esperado | Estado |
|---|---|---|
| GET /api/measurements | HTTP 200 | APROBADA |
| Parámetro limit | Restringe resultados | APROBADA |
| Filtro device_id | Filtra correctamente | APROBADA |
| Dispositivo inexistente | HTTP 404 | APROBADA |
| limit=0 | HTTP 422 | APROBADA |

## 5. Ejecución

Comando utilizado:

python -m pytest -q tests/test_api_queries.py

Resultado:

5 passed, 1 warning in 0.82s

Las cinco pruebas finalizaron correctamente.

Se presentó una advertencia de deprecación relacionada
con TestClient y httpx, sin afectar los resultados.

## 6. Evidencia A8

Archivo:

A8_01_pytest_5_pruebas_aprobadas.png

La captura demuestra la ejecución satisfactoria
de las cinco pruebas automatizadas.

Código fuente:

tests/test_api_queries.py

## 7. Conclusión

Se implementó una suite mínima de cinco pruebas
automatizadas para la API REST SmartDoor.

Las pruebas verifican consultas exitosas, límites,
filtros, dispositivos inexistentes y parámetros inválidos.

Se comprobó que las cinco pruebas funcionan correctamente
con una base de datos temporal e independiente.

La Fase 8 permite detectar regresiones en futuras
modificaciones de la API.
