
import sqlite3

import pytest
from fastapi.testclient import TestClient

from backend import database
from backend.main import app


# ==========================================
# CONFIGURACION DE BASE DE DATOS DE PRUEBAS
# ==========================================

@pytest.fixture
def client(tmp_path, monkeypatch):

    # Crear base de datos temporal
    db_path = tmp_path / "smartdoor_test.db"

    # Redirigir la conexion de SmartDoor
    monkeypatch.setattr(
        database,
        "DB_PATH",
        str(db_path)
    )

    conexion = sqlite3.connect(db_path)

    # ======================================
    # TABLA DEVICES
    # ======================================

    conexion.execute("""
        CREATE TABLE devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            name TEXT,
            location TEXT,
            enabled INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================
    # TABLA TELEMETRY
    # ======================================

    conexion.execute("""
        CREATE TABLE telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE NOT NULL,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            door_state TEXT NOT NULL,
            open_duration INTEGER NOT NULL,
            access_count INTEGER NOT NULL,
            alert_status TEXT NOT NULL
        )
    """)

    # ======================================
    # INSERTAR DISPOSITIVO DE PRUEBA
    # ======================================

    conexion.execute("""
        INSERT INTO devices (
            device_id,
            name,
            location,
            enabled
        )
        VALUES (?, ?, ?, ?)
    """, (
        "DOOR-TEST-001",
        "Puerta de prueba",
        "Laboratorio",
        1
    ))

    # ======================================
    # INSERTAR CINCO MEDICIONES
    # ======================================

    for i in range(1, 6):

        conexion.execute("""
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
            f"TEST-{i}",
            "DOOR-TEST-001",
            f"2026-10-25T10:00:{i:02d}Z",
            i,
            "CLOSED",
            0,
            1,
            "NORMAL"
        ))

    conexion.commit()
    conexion.close()

    # Crear cliente de pruebas FastAPI
    with TestClient(app) as test_client:
        yield test_client


# ==========================================
# PRUEBA 1 - GET MEASUREMENTS HTTP 200
# ==========================================

def test_get_measurements_200(client):

    respuesta = client.get(
        "/api/measurements"
    )

    assert respuesta.status_code == 200


# ==========================================
# PRUEBA 2 - LIMIT RESTRINGE RESULTADOS
# ==========================================

def test_limit_restringe_resultados(client):

    respuesta = client.get(
        "/api/measurements?limit=2"
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert len(datos["measurements"]) == 2


# ==========================================
# PRUEBA 3 - FILTRO POR DEVICE_ID
# ==========================================

def test_device_id_filtra_correctamente(client):

    respuesta = client.get(
        "/api/measurements?device_id=DOOR-TEST-001"
    )

    assert respuesta.status_code == 200

    mediciones = respuesta.json()["measurements"]

    assert len(mediciones) == 5

    assert all(
        medicion["device_id"] == "DOOR-TEST-001"
        for medicion in mediciones
    )


# ==========================================
# PRUEBA 4 - DISPOSITIVO INEXISTENTE 404
# ==========================================

def test_dispositivo_inexistente_404(client):

    respuesta = client.get(
        "/api/devices/NO-EXISTE"
    )

    assert respuesta.status_code == 404


# ==========================================
# PRUEBA 5 - LIMIT INVALIDO 422
# ==========================================

def test_limit_invalido_422(client):

    respuesta = client.get(
        "/api/measurements?limit=0"
    )

    assert respuesta.status_code == 422
