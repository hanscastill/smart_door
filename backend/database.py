import os
import sqlite3


# ==================================================
# CONFIGURACION SQLITE SMARTDOOR
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "database",
        "smartdoor.db"
    )
)


def obtener_conexion():
    conexion = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conexion.row_factory = sqlite3.Row

    # Esperar hasta 30 segundos si SQLite está ocupado
    conexion.execute("PRAGMA busy_timeout = 30000")

    # WAL mejora la concurrencia entre lecturas y escrituras
    conexion.execute("PRAGMA journal_mode = WAL")

    return conexion


def verificar_conexion():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tablas = [fila["name"] for fila in cursor.fetchall()]

    conexion.close()

    return {
        "database": DB_PATH,
        "tables": tablas
    }


def list_measurements(
    device_id: str | None = None,
    limit: int = 20,
    offset: int = 0
) -> list[dict]:
    """
    Consulta las mediciones almacenadas en SQLite
    con filtros y paginacion.
    """

    if not 1 <= limit <= 100:
        raise ValueError("limit debe estar entre 1 y 100")

    if offset < 0:
        raise ValueError("offset no puede ser negativo")

    conexion = obtener_conexion()

    try:
        consulta = """
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
        """

        parametros = []

        if device_id:
            consulta += " WHERE device_id = ?"
            parametros.append(device_id)

        consulta += " ORDER BY rowid DESC LIMIT ? OFFSET ?"
        parametros.extend([limit, offset])

        cursor = conexion.execute(
            consulta,
            parametros
        )

        return [dict(fila) for fila in cursor.fetchall()]

    finally:
        conexion.close()



# ==========================================
# FASE 3 - DISPOSITIVOS DESDE TELEMETRIA
# ==========================================

def list_devices() -> list[dict]:
    conexion = obtener_conexion()

    try:
        cursor = conexion.execute("""
            SELECT
                device_id,
                COUNT(*) AS measurement_count,
                MAX(timestamp) AS last_timestamp
            FROM telemetry
            GROUP BY device_id
            ORDER BY device_id
        """)

        return [dict(fila) for fila in cursor.fetchall()]

    finally:
        conexion.close()


def get_device_summary(device_id: str) -> dict | None:
    conexion = obtener_conexion()

    try:
        cursor = conexion.execute("""
            SELECT
                device_id,
                COUNT(*) AS measurement_count,
                MAX(timestamp) AS last_timestamp
            FROM telemetry
            WHERE device_id = ?
            GROUP BY device_id
        """, (device_id,))

        fila = cursor.fetchone()

        return dict(fila) if fila else None

    finally:
        conexion.close()
