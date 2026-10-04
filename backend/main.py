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