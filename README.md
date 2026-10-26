
# SmartDoor – Sistema IoT de monitoreo de puertas

## 1. Descripción

SmartDoor es un sistema IoT que permite simular múltiples sensores de puertas, transmitir telemetría, almacenar mediciones y consultar información mediante una API REST.

El proyecto incluye escenarios NORMAL y ALERT, persistencia SQLite, dashboard, alertas, reportes, gráficas, pruebas automatizadas y documentación técnica.

## 2. Arquitectura

Componentes principales:

- Simulador IoT desarrollado en Python.
- Backend FastAPI.
- Base de datos SQLite.
- API REST HTTP.
- Integración MQTT mediante Mosquitto.
- Dashboard web para visualización.
- Pruebas automatizadas con pytest.

Flujo principal:

Simulador IoT → HTTP POST → FastAPI → SQLite → HTTP GET → Cliente.

La integración MQTT constituye un mecanismo adicional de recepción de telemetría.

## 3. Requisitos

- Python 3.10 o superior.
- Git.
- Dependencias de backend/requirements.txt.
- Mosquitto para las pruebas que utilicen MQTT.

## 4. Instalación

Clonar el repositorio:

```bash
git clone https://github.com/hanscastill/smart_door.git
cd smart_door
```

Crear entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install -r backend/requirements.txt
```

### Inicializar la base de datos SQLite

Antes de iniciar el backend por primera vez, es necesario
crear las tablas utilizadas por SmartDoor.

Desde la raíz del proyecto, ejecutar:

```bash
python database/init_db.py
```

El inicializador crea las siguientes tablas:

- `devices`: almacena los dispositivos IoT registrados.
- `telemetry`: almacena las mediciones enviadas por el simulador.

Para comprobar que la inicialización se realizó correctamente,
verificar que aparezcan las tablas `devices` y `telemetry`
en la terminal.

**Nota:** El inicializador crea las tablas que no existen,
pero no modifica automáticamente las estructuras de tablas
antiguas. Si se utiliza una base de datos de una versión
anterior, puede requerirse una migración del esquema.

Una vez inicializada la base de datos, continuar con
la ejecución del backend.


## 5. Ejecutar el backend

Desde la raíz del proyecto:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Documentación Swagger:

http://127.0.0.1:8000/docs

## 6. Ejecutar el simulador

En otra terminal:

```bash
python simulator/smartdoor_simulator.py
```

El simulador utiliza la configuración definida en:

simulator/config.json

El backend debe estar ejecutándose para recibir telemetría HTTP.

## 7. Endpoints principales

| Método | Ruta | Propósito |
|---|---|---|
| GET | /api/devices | Consultar dispositivos |
| GET | /api/devices/{device_id} | Consultar dispositivo específico |
| GET | /api/measurements | Consultar mediciones |
| GET | /api/measurements?device_id=DOOR-001 | Filtrar por dispositivo |
| GET | /api/measurements?limit=10 | Limitar resultados |
| GET | /api/measurements?offset=10 | Paginar resultados |
| POST | /api/telemetry | Registrar telemetría |

## 8. Ejemplos de consultas GET

Consultar mediciones:

```bash
curl "http://127.0.0.1:8000/api/measurements"
```

Filtrar por dispositivo:

```bash
curl "http://127.0.0.1:8000/api/measurements?device_id=DOOR-001"
```

Limitar resultados:

```bash
curl "http://127.0.0.1:8000/api/measurements?limit=5"
```

Consultar dispositivo inexistente:

```bash
curl -i "http://127.0.0.1:8000/api/devices/NO-EXISTE"
```

## 9. Pruebas automatizadas

Ejecutar:

```bash
python -m pytest -q tests/test_api_queries.py
```

La suite mínima verifica:

1. GET /api/measurements responde HTTP 200.
2. El parámetro limit restringe resultados.
3. El filtro device_id funciona.
4. Un dispositivo inexistente responde HTTP 404.
5. Un límite inválido responde HTTP 422.

Resultado verificado en la Fase 8:

5 passed, 1 warning.

Las pruebas utilizan una base de datos temporal independiente.

## 10. Estado del proyecto

- Simulación IoT implementada.
- API REST funcional.
- Persistencia SQLite verificada.
- Consultas y filtros implementados.
- Regla de alertas corregida.
- Cinco pruebas automatizadas aprobadas.
- Evidencias técnicas de las fases anteriores disponibles.

Pendiente:

- Revisión de reproducibilidad por otro integrante.
- Registro de hallazgos y correcciones.
- Integración final de la rama de trabajo.

## 11. Evidencias

Las evidencias de la Guía 4 están organizadas en:

docs/evidencias/guia-4/

## 12. Integrantes

Proyecto académico SmartDoor.

Universidad de San Buenaventura – Facultad de Ingeniería.

Completar los nombres de los integrantes responsables antes de la entrega.