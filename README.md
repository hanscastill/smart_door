# SmartDoor - Sistema IoT de Monitoreo de Puertas

SmartDoor es un proyecto IoT orientado al monitoreo de sensores de puertas.

El sistema simula dispositivos IoT, genera telemetría y transmite actualmente la información mediante MQTT hacia un broker Mosquitto. El backend desarrollado con FastAPI procesa los mensajes y almacena la información de forma persistente en SQLite. La API REST mantiene comunicación HTTP para consultas y operaciones del sistema.

El proyecto también dispone de Dashboard web, módulo de alertas, reportes, gráficas y pruebas automáticas.

---

## 1. Objetivo del proyecto

Implementar una solución IoT capaz de:

- Simular múltiples sensores de puertas.
- Generar telemetría estructurada en formato JSON.
- Transmitir la telemetría de los dispositivos mediante MQTT.
- Validar la información recibida.
- Detectar estados normales y situaciones de alerta.
- Persistir la telemetría en SQLite.
- Consultar información mediante una API REST.
- Visualizar datos mediante un Dashboard.
- Generar reportes y gráficas.
- Ejecutar pruebas automáticas.
- Documentar la arquitectura y las decisiones técnicas.
.
---

## 2. Arquitectura general

El flujo principal de SmartDoor es:

Dispositivos IoT simulados 
↓ 
Broker MQTT - Mosquitto 
↓ 
Backend FastAPI 
↓ 
Validación del contrato JSON 
↓ 
Base de datos SQLite 
↓ 
API REST  .
↓ 
Dashboard / Alertas / Reportes / Gráficas

La documentación detallada de arquitectura se encuentra en:

`docs/arquitectura/arquitectura-backend.md`

Diagrama de arquitectura:

`docs/arquitectura/arquitectura-backend.png`

---

## 3. Estructura del proyecto

```text
smart_door/
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── templates/
│       ├── alertas.html
│       ├── dashboard.html
│       └── reportes.html
│
├── database/
│   ├── init_db.py
│   └── smartdoor.db
│
├── simulator/
│   ├── config.json
│   ├── smartdoor_simulator.py
│   └── tests/
│       └── test_simulator.py
│
├── tests/
│   ├── test_backend.py
│   └── test_smartdoor.py
│
├── docs/
│   ├── arquitectura/
│   │   ├── arquitectura-backend.md
│   │   └── arquitectura-backend.png
│   ├── decisiones/
│   │   └── persistencia.md
│   └── evidencias/
│
├── frontend/
├── README.md
├── LICENSE
└── .gitignore

```

---

## 4. Contrato JSON común

SmartDoor utiliza un contrato JSON común para la transmisión de telemetría entre los dispositivos simulados y el backend.

Ejemplo:

```json
{
  "message_id": "DOOR-001-000001",
  "device_id": "DOOR-001",
  "timestamp": "2026-09-19T05:52:04Z",
  "sequence": 1,
  "measurements": {
    "door_state": "OPEN",
    "open_duration": 30,
    "access_count": 1
  }
}

```

---

## 5. Configuración del simulador

La configuración del simulador se encuentra en:

`simulator/config.json`

El sistema simula los siguientes dispositivos:

- DOOR-001
- DOOR-002
- DOOR-003

La configuración permite controlar parámetros como el intervalo de envío, escenario de ejecución, probabilidad de apertura, tiempo para generar alertas y transporte de telemetría. Actualmente el transporte configurado es MQTT.

---

## 6. Escenario normal

SmartDoor permite generar lecturas correspondientes al funcionamiento normal del sensor.

Ejemplo:

- door_state: CLOSED
- open_duration: 0
- access_count: 0
- alert_status: NORMAL

Una puerta abierta durante un tiempo inferior al umbral establecido también puede considerarse una lectura normal.

---

## 7. Escenario de alerta

Cuando una puerta permanece abierta durante el tiempo establecido para generar una alerta, SmartDoor registra:

- door_state: OPEN
- alert_status: ALERT

El backend recibe, valida y procesa esta información antes de almacenarla en la base de datos.

---

## 8. Persistencia

SmartDoor utiliza SQLite como mecanismo de persistencia.

La base de datos principal se encuentra en:

`database/smartdoor.db`

La decisión técnica sobre el mecanismo de persistencia está documentada en:

`docs/decisiones/persistencia.md`

La información almacenada puede posteriormente ser consultada mediante la API REST, el Dashboard, el módulo de alertas y los reportes.

---

## 9. API y FastAPI

El backend de SmartDoor está desarrollado con FastAPI.

La API permite recibir, validar, almacenar y consultar la telemetría generada por los dispositivos IoT.

Entre las funciones implementadas se encuentran:

- Verificación del estado de la API.
- Consulta de dispositivos registrados.
- Consulta general de lecturas.
- Consulta de telemetría por dispositivo.
- Recepción y procesamiento de telemetría mediante MQTT.
- Validación de los datos recibidos.
- Persistencia de información en SQLite.

---

## 10. Comunicación MQTT

SmartDoor utiliza MQTT para la comunicación de telemetría entre los dispositivos simulados y el backend.

El broker utilizado es Mosquitto.

Tópico MQTT:

`smartdoor/telemetry`

Los dispositivos simulados publican telemetría en este tópico y el backend procesa los mensajes recibidos.

---

## 11. Pruebas automáticas

SmartDoor cuenta con pruebas automáticas desarrolladas con Pytest.

Las pruebas pueden ejecutarse mediante:

```bash
pytest -v

```

---

## 12. Visualización

SmartDoor dispone de una interfaz web para visualizar la información procesada.

El sistema incluye:

- Dashboard principal.
- Estado de los dispositivos.
- Historial de lecturas.
- Módulo de alertas.
- Reportes estadísticos.
- Gráfica del tiempo de apertura.
- Gráfica de actividad de accesos.
- Comparación entre alertas y estados normales.

---

## 13. Tecnologías utilizadas

El proyecto utiliza las siguientes tecnologías:

- Python
- FastAPI
- SQLite
- MQTT
- Mosquitto
- HTTP
- REST API
- JSON
- Pytest
- HTML
- Git
- GitHub
- GitHub Codespaces
- Mermaid

---

## 14. Documentación técnica

La documentación de arquitectura se encuentra en:

`docs/arquitectura/arquitectura-backend.md`

El diagrama gráfico de arquitectura se encuentra en:

`docs/arquitectura/arquitectura-backend.png`

La decisión sobre el mecanismo de persistencia se encuentra en:

`docs/decisiones/persistencia.md`

Las evidencias del proyecto se encuentran en:

`docs/evidencias/`

---

## 15. Estado del proyecto

SmartDoor cuenta con simulación de múltiples dispositivos IoT, configuración externa, contrato JSON común, transmisión de telemetría mediante MQTT, broker Mosquitto, backend FastAPI, API REST mediante HTTP, persistencia SQLite, validación de datos, escenarios NORMAL y ALERT, Dashboard, módulo de alertas, reportes, gráficas, pruebas automáticas y documentación técnica.

