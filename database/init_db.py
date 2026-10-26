
import sqlite3
import os

# ==========================================
# SMARTDOOR - INICIALIZACION SQLITE
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smartdoor.db")


def inicializar_base_datos():
    conexion = sqlite3.connect(DB_PATH)

    try:
        cursor = conexion.cursor()

        # CREAR TABLA DE DISPOSITIVOS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # CREAR TABLA DE TELEMETRIA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT NOT NULL UNIQUE,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                door_state TEXT NOT NULL,
                open_duration REAL NOT NULL,
                access_count INTEGER NOT NULL,
                alert_status TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexion.commit()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """)

        print("====================================")
        print(" SMARTDOOR - BASE DE DATOS SQLITE")
        print("====================================")
        print()
        print("Base de datos:", DB_PATH)
        print()
        print("Tablas disponibles:")

        for tabla in cursor.fetchall():
            print(" -", tabla[0])

        print()
        print("Inicializacion finalizada correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error:", error)
        raise

    finally:
        conexion.close()


if __name__ == "__main__":
    inicializar_base_datos()
