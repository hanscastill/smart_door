from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.database import obtener_conexion

from backend.schemas import (
    TelemetryCreate,
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse
)
import sqlite3
import json
import threading
import paho.mqtt.client as mqtt

# ==================================================
# FASTAPI SMARTDOOR
# ==================================================

app = FastAPI(
    title="SmartDoor API",
    description="API REST para gestion de dispositivos y telemetria SmartDoor",
    version="1.0.0"
)
templates = Jinja2Templates(directory="backend/templates")

# ==================================================
# CONFIGURACION MQTT SMARTDOOR
# ==================================================

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "smartdoor/telemetry"


def on_mqtt_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):
    print("=== MQTT SMARTDOOR ===")

    if reason_code == 0:
        print("Conectado correctamente al broker MQTT")
        print("Broker:", MQTT_BROKER)
        print("Puerto:", MQTT_PORT)
        print("Topic:", MQTT_TOPIC)

        client.subscribe(MQTT_TOPIC)

        print(
            "Suscripcion MQTT realizada correctamente"
        )

    else:
        print(
            "Error conectando al broker MQTT:",
            reason_code
        )


def on_mqtt_message(client, userdata, msg):

    conexion = None

    try:
        mensaje = msg.payload.decode("utf-8")
        datos = json.loads(mensaje)

        print("\nNUEVA TELEMETRIA RECIBIDA POR MQTT")
        print("Topic:", msg.topic)
        print("Dispositivo:", datos.get("device_id"))
        print("Message ID:", datos.get("message_id"))

        # Validar campos principales
        campos_obligatorios = [
            "message_id",
            "device_id",
            "timestamp",
            "sequence",
            "measurements"
        ]

        faltantes = [
            campo for campo in campos_obligatorios
            if campo not in datos
        ]

        if faltantes:
            print("ERROR MQTT - Faltan campos:", faltantes)
            return

        measurements = datos["measurements"]

        if not isinstance(measurements, dict):
            print("ERROR MQTT - measurements debe ser un objeto JSON")
            return

        campos_medicion = [
            "door_state",
            "open_duration",
            "access_count"
        ]

        faltantes_medicion = [
            campo for campo in campos_medicion
            if campo not in measurements
        ]

        if faltantes_medicion:
            print(
                "ERROR MQTT - Faltan campos en measurements:",
                faltantes_medicion
            )
            return

        # Validar tipos
        if not isinstance(datos["sequence"], int):
            print("ERROR MQTT - sequence debe ser integer")
            return

        if not isinstance(measurements["open_duration"], (int, float)):
            print("ERROR MQTT - open_duration debe ser numerico")
            return

        if not isinstance(measurements["access_count"], int):
            print("ERROR MQTT - access_count debe ser integer")
            return

        if not isinstance(measurements["door_state"], str):
            print("ERROR MQTT - door_state debe ser string")
            return

        door_state = measurements["door_state"]
        open_duration = measurements["open_duration"]
        access_count = measurements["access_count"]

        # Reglas SmartDoor
        if door_state not in ["OPEN", "CLOSED"]:
            print("ERROR MQTT - door_state invalido")
            return

        if door_state == "CLOSED" and open_duration != 0:
            print(
                "ERROR MQTT - Una puerta CLOSED "
                "debe tener open_duration = 0"
            )
            return

        # Calcular alerta
        if door_state == "OPEN" and open_duration > 30:
            alert_status = "ALERT"
        else:
            alert_status = "NORMAL"

        # Guardar en SQLite
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO telemetry (
                message_id,
                device_id,
                timestamp,
                sequence,
                door_state,
                open_duration,
                access_count,
                alert_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos["message_id"],
            datos["device_id"],
            datos["timestamp"],
            datos["sequence"],
            door_state,
            open_duration,
            access_count,
            alert_status
        ))

        conexion.commit()

        print("----------------------------------------")
        print("TELEMETRIA MQTT GUARDADA EN SQLITE")
        print("Message ID:", datos["message_id"])
        print("Device ID:", datos["device_id"])
        print("Estado:", door_state)
        print("Tiempo abierta:", open_duration)
        print("Accesos:", access_count)
        print("Alerta:", alert_status)
        print("----------------------------------------")

    except sqlite3.IntegrityError as error:
        if conexion:
            conexion.rollback()
        print("MQTT - Message ID duplicado:", error)

    except json.JSONDecodeError as error:
        print("MQTT - JSON invalido:", error)

    except Exception as error:
        if conexion:
            conexion.rollback()
        print("ERROR procesando MQTT:", error)

    finally:
        if conexion:
            conexion.close()


def iniciar_mqtt():

    try:
        print("Iniciando cliente MQTT SmartDoor...")

        cliente = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        cliente.on_connect = on_mqtt_connect
        cliente.on_message = on_mqtt_message

        cliente.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

        cliente.loop_forever()

    except Exception as error:
        print(
            "Error iniciando cliente MQTT:",
            error
        )


hilo_mqtt = threading.Thread(
    target=iniciar_mqtt,
    daemon=True
)

hilo_mqtt.start()

print("Cliente MQTT iniciado en segundo plano")
# ==================================================
# ENDPOINT PRINCIPAL
# ==================================================

@app.get("/")
def inicio():
    return {
        "status": "success",
        "message": "SmartDoor API funcionando correctamente",
        "version": "1.0.0"
    }
# ================================================
# DASHBOARD SMARTDOOR
# ================================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )
# ============================================
# REPORTES SMARTDOOR
# ============================================

@app.get("/reportes", response_class=HTMLResponse)
def reportes(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="reportes.html"
    )
# ============================================
# ALERTAS SMARTDOOR
# ============================================

@app.get("/alertas", response_class=HTMLResponse)
def alertas(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="alertas.html"
    )


# ============================================
# API DE REPORTES SMARTDOOR
# GET /api/reportes
# ============================================

@app.get("/api/reportes")
def obtener_reportes():

    conexion = obtener_conexion()

    try:

        # Total de lecturas
        total_lecturas = conexion.execute(
            "SELECT COUNT(*) AS total FROM telemetry"
        ).fetchone()["total"]

        # Total de alertas
        total_alertas = conexion.execute(
            """
            SELECT COUNT(*) AS total
            FROM telemetry
            WHERE alert_status = 'ALERT'
            """
        ).fetchone()["total"]

        # Total de estados normales
        total_normal = conexion.execute(
            """
            SELECT COUNT(*) AS total
            FROM telemetry
            WHERE alert_status = 'NORMAL'
            """
        ).fetchone()["total"]

        # Tiempo promedio de apertura
        tiempo_promedio = conexion.execute(
            """
            SELECT ROUND(AVG(open_duration), 2) AS promedio
            FROM telemetry
            """
        ).fetchone()["promedio"]

        # Tiempo máximo de apertura
        tiempo_maximo = conexion.execute(
            """
            SELECT MAX(open_duration) AS maximo
            FROM telemetry
            """
        ).fetchone()["maximo"]

        # Total de accesos
        total_accesos = conexion.execute(
            """
            SELECT SUM(access_count) AS total
            FROM telemetry
            """
        ).fetchone()["total"]

        return {
            "status": "success",
            "reporte": {
                "total_lecturas": total_lecturas,
                "total_alertas": total_alertas,
                "total_normal": total_normal,
                "tiempo_promedio_abierta": tiempo_promedio or 0,
                "tiempo_maximo_abierta": tiempo_maximo or 0,
                "total_accesos": total_accesos or 0
            }
        }

    except sqlite3.Error as error:

        return {
            "status": "error",
            "message": "Error consultando reportes en SQLite",
            "error": str(error)
        }

    finally:
        conexion.close()
# ==================================================
# HEALTH CHECK
# ==================================================
# ==================================================
# API DE ALERTAS SMARTDOOR
# GET /api/alertas
# ==================================================

@app.get("/api/alertas")
def obtener_alertas():

    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id,
                message_id,
                device_id,
                timestamp,
                sequence,
                door_state,
                open_duration,
                access_count,
                alert_status
            FROM telemetry
            WHERE alert_status = 'ALERT'
            ORDER BY id DESC
        """)

        registros = [
            dict(fila)
            for fila in cursor.fetchall()
        ]

        return {
            "status": "success",
            "total": len(registros),
            "alertas": registros
        }

    except sqlite3.Error as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error consultando alertas: {error}"
        )

    finally:
        conexion.close()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "SmartDoor API"
    }

# ==================================================
# DISPOSITIVOS SMARTDOOR
# ==================================================


# --------------------------------------------------
# CREAR DISPOSITIVO
# POST /api/devices
# --------------------------------------------------

@app.post("/api/devices", status_code=201)
def crear_dispositivo(device: DeviceCreate):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO devices (
                device_id,
                name,
                location,
                enabled
            )
            VALUES (?, ?, ?, ?)
        """, (
            device.device_id,
            device.name,
            device.location,
            1 if device.enabled else 0
        ))

        conexion.commit()
        conexion.close()

    except sqlite3.IntegrityError:
        conexion.rollback()
        conexion.close()

        raise HTTPException(
            status_code=409,
            detail="El message_id ya existe"
        )

        nuevo_id = cursor.lastrowid

        cursor.execute("""
            SELECT
                id,
                device_id,
                name,
                location,
                enabled,
                created_at
            FROM devices
            WHERE id = ?
        """, (nuevo_id,))

        registro = cursor.fetchone()

        return {
            "status": "success",
            "message": "Dispositivo SmartDoor creado correctamente",
            "device": dict(registro)
        }

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=409,
            detail="El device_id ya existe"
        )

    finally:
        conexion.close()


# --------------------------------------------------
# LISTAR DISPOSITIVOS
# GET /api/devices
# --------------------------------------------------

@app.get("/api/devices")
def listar_dispositivos():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            device_id,
            name,
            location,
            enabled,
            created_at
        FROM devices
        ORDER BY id ASC
    """)

    dispositivos = [
        dict(fila)
        for fila in cursor.fetchall()
    ]

    conexion.close()

    return {
        "status": "success",
        "total": len(dispositivos),
        "devices": dispositivos
    }
# ------------------------------------------------
# CONSULTAR DISPOSITIVO POR DEVICE_ID
# GET /api/devices/{device_id}
# ------------------------------------------------

@app.get("/api/devices/{device_id}")
def obtener_dispositivo(device_id: str):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            device_id,
            name,
            location,
            enabled,
            created_at
        FROM devices
        WHERE device_id = ?
    """, (device_id,))

    fila = cursor.fetchone()

    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo SmartDoor no encontrado"
        )

    return {
        "status": "success",
        "device": dict(fila)
    }

# ------------------------------------------------
# ACTUALIZAR DISPOSITIVO SMARTDOOR
# PUT /api/devices/{device_id}
# ------------------------------------------------

@app.put("/api/devices/{device_id}")
def actualizar_dispositivo(
    device_id: str,
    dispositivo: DeviceUpdate
):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar que el dispositivo exista
    cursor.execute(
        "SELECT * FROM devices WHERE device_id = ?",
        (device_id,)
    )

    existente = cursor.fetchone()

    if existente is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Dispositivo SmartDoor no encontrado"
        )

    # Actualizar dispositivo
    cursor.execute("""
        UPDATE devices
        SET
            name = ?,
            location = ?,
            enabled = ?
        WHERE device_id = ?
    """, (
        dispositivo.name,
        dispositivo.location,
        dispositivo.enabled,
        device_id
    ))

    conexion.commit()

    # Consultar resultado actualizado
    cursor.execute("""
        SELECT
            id,
            device_id,
            name,
            location,
            enabled,
            created_at
        FROM devices
        WHERE device_id = ?
    """, (device_id,))

    actualizado = cursor.fetchone()

    conexion.close()

    return {
        "status": "success",
        "message": "Dispositivo SmartDoor actualizado correctamente",
        "device": dict(actualizado)
    }
# ================================================
# ELIMINAR DISPOSITIVO SMARTDOOR
# DELETE /api/devices/{device_id}
# ================================================

@app.delete("/api/devices/{device_id}")
def eliminar_dispositivo(device_id: str):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Verificar si el dispositivo existe
    cursor.execute(
        "SELECT * FROM devices WHERE device_id = ?",
        (device_id,)
    )

    dispositivo = cursor.fetchone()

    if dispositivo is None:
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Dispositivo SmartDoor no encontrado"
        )

    # Eliminar dispositivo
    cursor.execute(
        "DELETE FROM devices WHERE device_id = ?",
        (device_id,)
    )

    conexion.commit()
    conexion.close()

    return {
        "status": "success",
        "message": "Dispositivo SmartDoor eliminado correctamente",
        "device_id": device_id
    }


# ==================================================
# LISTAR TELEMETRIA
# ==================================================

@app.get("/api/telemetry")
def listar_telemetria():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            message_id,
            device_id,
            timestamp,
            sequence,
            door_state,
            open_duration,
            access_count,
            alert_status
        FROM telemetry
        ORDER BY rowid DESC
    """)

    registros = [
        dict(fila)
        for fila in cursor.fetchall()
    ]

    conexion.close()

    return {
        "status": "success",
        "total": len(registros),
        "telemetry": registros
    }

# ==================================================
# LECTURAS PARA REPORTES Y GRAFICAS
# GET /api/lecturas
# ==================================================

@app.get("/api/lecturas")
def listar_lecturas():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            SELECT
                message_id,
                device_id,
                timestamp,
                sequence,
                door_state,
                open_duration,
                access_count,
                alert_status
            FROM telemetry
            ORDER BY rowid DESC
            LIMIT 100
        """)

        registros = [
            dict(fila)
            for fila in cursor.fetchall()
        ]

        return {
            "status": "success",
            "total": len(registros),
            "lecturas": registros
        }

    except sqlite3.Error as error:

        raise HTTPException(
            status_code=500,
            detail=f"Error consultando lecturas: {error}"
        )

    finally:
        conexion.close()

# ==================================================
# CONSULTAR TELEMETRIA POR DISPOSITIVO
# ==================================================

@app.get("/api/devices/{device_id}/telemetry")
def telemetria_dispositivo(device_id: str):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            message_id,
            device_id,
            timestamp,
            sequence,
            door_state,
            open_duration,
            access_count,
            alert_status
        FROM telemetry
        WHERE device_id = ?
        ORDER BY rowid DESC
    """, (device_id,))

    registros = [
        dict(fila)
        for fila in cursor.fetchall()
    ]

    conexion.close()

    return {
        "status": "success",
        "device_id": device_id,
        "total": len(registros),
        "telemetry": registros
    }


# ==================================================
# REGISTRAR TELEMETRIA
# ==================================================

@app.post("/api/telemetry", status_code=201)
def registrar_telemetria(datos: TelemetryCreate):

    door_state = datos.measurements.door_state
    open_duration = datos.measurements.open_duration
    access_count = datos.measurements.access_count

    # Regla de negocio SmartDoor
    if door_state == "CLOSED" and open_duration != 0:
        raise HTTPException(
            status_code=400,
            detail="Una puerta CLOSED debe tener open_duration igual a 0"
        )

    # Calcular alerta
    if door_state == "OPEN" and open_duration > 30:
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO telemetry (
                message_id,
                device_id,
                timestamp,
                sequence,
                door_state,
                open_duration,
                access_count,
                alert_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos.message_id,
            datos.device_id,
            datos.timestamp,
            datos.sequence,
            door_state,
            open_duration,
            access_count,
            alert_status
        ))

        conexion.commit()
        conexion.close()

    except sqlite3.IntegrityError:
        conexion.rollback()
        conexion.close()

        raise HTTPException(
            status_code=409,
            detail="El message_id ya existe"
        )

    return {
        "status": "success",
        "message": "Telemetria registrada correctamente",
        "message_id": datos.message_id,
        "device_id": datos.device_id,
        "alert_status": alert_status
    }