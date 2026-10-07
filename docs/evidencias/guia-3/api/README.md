# Evidencia API REST - SmartDoor

## Objetivo

Documentar y comprobar el funcionamiento de la API REST desarrollada con FastAPI para SmartDoor.

## Backend

El backend principal se encuentra en:

`backend/main.py`

El servidor puede ejecutarse mediante Uvicorn.

Ejemplo:

`python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload`

## Health Check

SmartDoor dispone del endpoint:

`GET /health`

Este endpoint permite comprobar que la API se encuentra activa.

## Dispositivos

La API permite gestionar y consultar los dispositivos SmartDoor.

Entre las operaciones implementadas se encuentran:

- Crear dispositivos.
- Listar dispositivos.
- Consultar un dispositivo.
- Actualizar dispositivos.
- Eliminar dispositivos.

## Telemetría

La API permite consultar la telemetría almacenada.

Entre los endpoints implementados se encuentran consultas generales y consultas específicas por dispositivo.

Ejemplo:

`GET /api/devices/{device_id}/telemetry`

## Recepción de telemetría

SmartDoor dispone de un endpoint para recibir telemetría mediante HTTP:

`POST /api/telemetry`

Aunque el transporte configurado actualmente para el simulador es MQTT, la API REST conserva HTTP para consultas y operaciones del sistema.

## Reportes y alertas

El backend también proporciona información para:

- Dashboard.
- Reportes.
- Alertas.
- Historial de telemetría.

## Persistencia

Los datos procesados por el backend se almacenan en:

`database/smartdoor.db`

## Resultado

La API REST permite administrar dispositivos, consultar telemetría, comprobar el estado del servicio y proporcionar información al Dashboard, reportes y módulo de alertas.

Arquitectura comprobada:

MQTT → FastAPI → SQLite → API REST → Dashboard
