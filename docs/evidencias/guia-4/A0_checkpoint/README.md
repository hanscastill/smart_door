# Evidencia A0 - Checkpoint técnico SmartDoor

## Proyecto
SmartDoor - Sistema IoT de monitoreo de puertas.

## Objetivo
Verificar que el backend recibe y almacena correctamente
la telemetría generada por el simulador.

## Pruebas realizadas

1. Inicio del backend mediante Uvicorn: exitoso.
2. GET /health: HTTP 200 OK.
3. Ejecución del simulador SmartDoor mediante HTTP.
4. POST /api/telemetry: HTTP 201 Created.
5. Consulta de registros en SQLite: exitosa.

## Base de datos
Ruta: database/smartdoor.db
Tabla: telemetry

## Lecturas verificadas

| Dispositivo | Sequence | Estado | Alerta |
|---|---:|---|---|
| DOOR-001 | 99530 | OPEN | NORMAL |
| DOOR-002 | 99533 | CLOSED | NORMAL |
| DOOR-003 | 99532 | OPEN | NORMAL |

## Resultado
Se comprobó que las tres lecturas generadas
por el simulador quedaron almacenadas en SQLite.

## Observación
La prueba se realizó mediante transporte HTTP.
La conexión MQTT requiere un broker disponible.

## Conclusión
El checkpoint técnico de la Fase 0 se completó
satisfactoriamente. SmartDoor está preparado
para implementar las consultas REST de la Guía 4.
