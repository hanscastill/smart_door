# Evidencia SQLite - SmartDoor

## Objetivo

Comprobar que la telemetría recibida por SmartDoor se almacena correctamente de forma persistente en SQLite.

## Base de datos

SmartDoor utiliza SQLite como mecanismo de persistencia.

Base de datos utilizada:

`database/smartdoor.db`

La información de los dispositivos IoT se almacena principalmente en la tabla:

`telemetry`

## Información almacenada

Cada registro de telemetría contiene información como:

- id
- message_id
- device_id
- timestamp
- sequence
- door_state
- open_duration
- access_count
- alert_status

## Dispositivos comprobados

Se verificó almacenamiento de telemetría para:

- DOOR-001
- DOOR-002
- DOOR-003

## Persistencia mediante MQTT

Los dispositivos publican la telemetría mediante MQTT en el tópico:

`smartdoor/telemetry`

El backend FastAPI recibe los mensajes y almacena los datos procesados en SQLite.

## Estados almacenados

Se comprobaron registros con estados:

- NORMAL
- ALERT

Una puerta cerrada registra normalmente `open_duration = 0` y estado `NORMAL`.

Una puerta que permanece abierta por encima del umbral configurado puede registrar estado `ALERT`.

## Resultado

Las pruebas realizadas demuestran que SmartDoor almacena correctamente en SQLite la telemetría recibida mediante MQTT.

Flujo validado:

Dispositivos IoT → MQTT → Mosquitto → FastAPI → SQLite
