import sqlite3
import os

# ==========================================
# RUTA DE LA BASE DE DATOS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "smartdoor.db")


# ==========================================
# CONECTAR A SQLITE
# ==========================================

conexion = sqlite3.connect(DB_PATH)

cursor = conexion.cursor()


# ==========================================
# CREAR TABLA DE TELEMETRIA
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    device_id TEXT NOT NULL,

    timestamp TEXT NOT NULL,

    door_state TEXT NOT NULL,

    open_duration INTEGER NOT NULL,

    access_count INTEGER NOT NULL,

    alert_status TEXT NOT NULL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

)
""")


# ==========================================
# GUARDAR CAMBIOS
# ==========================================

conexion.commit()


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

print("======================================")
print(" SMARTDOOR - BASE DE DATOS SQLITE")
print("======================================")
print()
print("Base de datos:")
print(DB_PATH)
print()
print("Tabla 'telemetry' creada correctamente.")


# ==========================================
# MOSTRAR TABLAS EXISTENTES
# ==========================================

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

tablas = cursor.fetchall()

print()
print("Tablas disponibles:")

for tabla in tablas:
    print(" -", tabla[0])


# ==========================================
# CERRAR CONEXION
# ==========================================

conexion.close()

print()
print("Inicializacion finalizada correctamente.")