# Evidencia MQTT - SmartDoor

## Objetivo

Comprobar la comunicación MQTT entre los dispositivos IoT simulados y el backend de SmartDoor.

## Broker MQTT

El proyecto utiliza Mosquitto como broker MQTT.

Configuración utilizada:

- Broker: 127.0.0.1
- Puerto: 1883
- Tópico: smartdoor/telemetry

## Flujo de comunicación

El flujo implementado es:

Dispositivo IoT simulado
→ publica telemetría MQTT
→ Mosquitto
→ tópico smartdoor/telemetry
→ Backend FastAPI
→ validación de telemetría
→ SQLite

## Dispositivos utilizados

Durante las pruebas se utilizaron tres dispositivos:

- DOOR-001
- DOOR-002
- DOOR-003

## Publicación MQTT

El simulador `smartdoor_simulator.py` genera la telemetría de cada dispositivo y la publica mediante MQTT.

Durante las pruebas se verificaron mensajes como:

- MQTT publicado correctamente: DOOR-001
- MQTT publicado correctamente: DOOR-002
- MQTT publicado correctamente: DOOR-003

## Recepción en FastAPI

El backend se encuentra suscrito al tópico:

`smartdoor/telemetry`

Al recibir un mensaje MQTT, procesa el JSON recibido, valida sus datos y registra la telemetría en SQLite.

Se verificaron mensajes de recepción y almacenamiento como:

- NUEVA TELEMETRIA RECIBIDA POR MQTT
- TELEMETRIA MQTT GUARDADA EN SQLITE

## Estados comprobados

Se comprobaron lecturas en estado:

- NORMAL
- ALERT

Una puerta abierta durante un tiempo superior al umbral configurado genera una alerta.

## Resultado

La prueba demuestra correctamente la integración:

MQTT → Mosquitto → FastAPI → SQLite

La comunicación MQTT se encuentra operativa para los tres dispositivos SmartDoor.
