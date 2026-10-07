# Evidencias - Guía 3 SmartDoor

Este directorio reúne las evidencias técnicas y funcionales del proyecto SmartDoor.

## 1. MQTT
Evidencias de conexión con Mosquitto, publicación y recepción de telemetría mediante el tópico `smartdoor/telemetry`.

## 2. Simulador IoT
Evidencias de ejecución de los dispositivos:
- DOOR-001
- DOOR-002
- DOOR-003

## 3. API FastAPI
Evidencias del backend, endpoints REST y procesamiento de telemetría.

## 4. SQLite
Evidencias de persistencia y consultas de telemetría almacenada.

## 5. Pruebas
Evidencias de pruebas automáticas ejecutadas con Pytest.

## 6. Dashboard
Evidencias del Dashboard, alertas, reportes y gráficas.

## 7. GitHub
Evidencias de commits, push y estado final del repositorio.

## Flujo validado

Dispositivos IoT simulados
→ MQTT / Mosquitto
→ FastAPI
→ Validación
→ SQLite
→ API REST
→ Dashboard / Alertas / Reportes
