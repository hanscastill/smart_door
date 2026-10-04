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