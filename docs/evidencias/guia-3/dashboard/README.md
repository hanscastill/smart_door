# Evidencia Dashboard - SmartDoor

## Objetivo

Documentar la interfaz web utilizada para visualizar la información procesada por SmartDoor.

## Dashboard principal

SmartDoor dispone de un Dashboard web proporcionado por el backend FastAPI.

La plantilla principal se encuentra en:

`backend/templates/dashboard.html`

El Dashboard permite visualizar información relacionada con los dispositivos IoT y su telemetría.

## Módulo de alertas

La plantilla correspondiente se encuentra en:

`backend/templates/alertas.html`

Este módulo permite visualizar las lecturas que presentan condiciones de alerta.

## Módulo de reportes

La plantilla correspondiente se encuentra en:

`backend/templates/reportes.html`

Los reportes permiten analizar la información almacenada en SQLite.

## Información visualizada

La interfaz utiliza la telemetría procesada por SmartDoor para presentar información como:

- Dispositivos monitoreados.
- Estado de las puertas.
- Tiempo de apertura.
- Cantidad de accesos.
- Estado NORMAL o ALERT.
- Historial de lecturas.
- Reportes estadísticos.
- Gráficas.

## Flujo de información

La información mostrada en la interfaz sigue el flujo:

Dispositivos IoT → MQTT → Mosquitto → FastAPI → SQLite → Dashboard

## Resultado

El Dashboard complementa la API REST permitiendo visualizar de forma gráfica y organizada la información generada por los sensores SmartDoor.

El sistema dispone de:

- Dashboard.
- Alertas.
- Reportes.
- Gráficas.
