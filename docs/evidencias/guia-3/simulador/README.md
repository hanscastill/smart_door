# Evidencia del Simulador IoT - SmartDoor

## Objetivo

Comprobar el funcionamiento del simulador de sensores de puertas utilizado por SmartDoor.

## Simulador principal

El simulador se encuentra en:

`simulator/smartdoor_simulator.py`

La configuración externa se encuentra en:

`simulator/config.json`

## Dispositivos simulados

Actualmente SmartDoor simula tres dispositivos:

- DOOR-001
- DOOR-002
- DOOR-003

Cada dispositivo mantiene su propio estado y secuencia de telemetría.

## Telemetría generada

El simulador genera información como:

- message_id
- device_id
- timestamp
- sequence
- door_state
- open_duration
- access_count
- alert_status

## Escenarios

El simulador permite representar estados NORMAL y ALERT.

Ejemplo de estado normal:

- door_state: CLOSED
- open_duration: 0
- alert_status: NORMAL

Ejemplo de alerta:

- door_state: OPEN
- open_duration superior al umbral configurado
- alert_status: ALERT

## Transporte

El transporte de telemetría configurado actualmente es:

`mqtt`

Los dispositivos publican sus mensajes en:

`smartdoor/telemetry`

El broker utilizado es Mosquitto.

## Resultado

Se verificó que DOOR-001, DOOR-002 y DOOR-003 generan telemetría correctamente y publican sus mensajes mediante MQTT.

Flujo del simulador:

DOOR-001 / DOOR-002 / DOOR-003 → MQTT → Mosquitto → FastAPI → SQLite
