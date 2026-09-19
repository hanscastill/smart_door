from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# ==========================================
# CONFIGURACION DE SQLITE
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "smartdoor.db"
)

DB_PATH = os.path.abspath(DB_PATH)


def obtener_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

lecturas = []
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/")
def inicio():
    return jsonify({
        "sistema": "SmartDoor",
        "estado": "API funcionando correctamente"
    })
# ============================================================
# API DE TELEMETRIA IoT
# POST /api/telemetry
# ============================================================

@app.route("/api/telemetry", methods=["POST"])
def recibir_telemetria():

    # Obtener JSON enviado por el simulador
    datos = request.get_json(silent=True)

    # --------------------------------------------------------
    # Validar que exista un JSON
    # --------------------------------------------------------
    if not datos:
        return jsonify({
            "status": "error",
            "message": "No se recibió información JSON"
        }), 400

    # --------------------------------------------------------
    # Campos obligatorios
    # --------------------------------------------------------
    campos_obligatorios = [
        "message_id",
        "device_id",
        "timestamp",
        "sequence",
        "measurements"
    ]

    faltantes = [
        campo
        for campo in campos_obligatorios
        if campo not in datos
    ]

    if faltantes:
        return jsonify({
            "status": "error",
            "message": "Faltan campos obligatorios",
            "fields": faltantes
        }), 400

    # --------------------------------------------------------
    # Validar measurements
    # --------------------------------------------------------
    measurements = datos["measurements"]

    if not isinstance(measurements, dict):
        return jsonify({
            "status": "error",
            "message": "measurements debe ser un objeto JSON"
        }), 400

    campos_medicion = [
        "door_state",
        "open_duration",
        "access_count"
    ]

    faltantes_medicion = [
        campo
        for campo in campos_medicion
        if campo not in measurements
    ]

    if faltantes_medicion:
        return jsonify({
            "status": "error",
            "message": "Faltan campos en measurements",
            "fields": faltantes_medicion
        }), 400

    # --------------------------------------------------------
    # Guardar temporalmente la lectura
    # --------------------------------------------------------
    lecturas.append(datos)

        # ==================================================
    # GUARDAR TELEMETRIA EN SQLITE
    # ==================================================
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
    datos["message_id"],
    datos["device_id"],
    datos["timestamp"],
    datos["sequence"],
    measurements["door_state"],
    measurements["open_duration"],
    measurements["access_count"],
    measurements["alert_status"]
))

        
        conexion.commit()
        conexion.close()

        print("Telemetria guardada correctamente en SQLite.")

    except sqlite3.IntegrityError as error:
        print("ERROR DE INTEGRIDAD SQLITE:", error)

        return jsonify({
            "status": "error",
            "message": "Error de integridad en SQLite",
            "error": str(error),
            "message_id": datos["message_id"]
        }), 409

    except sqlite3.OperationalError as error:
        print("Error operativo de SQLite:", error)

        return jsonify({
            "status": "error",
            "message": "Error operativo de SQLite",
            "error": str(error)
        }), 500

    except Exception as error:
        print("Error guardando telemetria en SQLite:", error)

        return jsonify({
            "status": "error",
            "message": "Error guardando telemetria en SQLite",
            "error": str(error)
        }), 500


        if 'conexion' in locals():
            conexion.close()

    # --------------------------------------------------------
    # Mostrar evidencia en terminal
    # --------------------------------------------------------
    print("\n" + "=" * 55)
    print("NUEVA TELEMETRIA RECIBIDA")
    print("=" * 55)

    print("Message ID :", datos["message_id"])
    print("Device ID  :", datos["device_id"])
    print("Timestamp  :", datos["timestamp"])
    print("Sequence   :", datos["sequence"])
    print("Estado     :", measurements["door_state"])
    print("Tiempo     :", measurements["open_duration"])
    print("Aperturas  :", measurements["access_count"])

    print("=" * 55)

    # --------------------------------------------------------
    # Respuesta HTTP
    # --------------------------------------------------------
    return jsonify({
        "status": "success",
        "message": "Telemetría recibida correctamente",
        "message_id": datos["message_id"],
        "device_id": datos["device_id"],
        "sequence": datos["sequence"]
    }), 201



@app.route("/api/sensor", methods=["POST"])
def recibir_datos_sensor():

    datos = request.get_json()

    lecturas.append(datos)

    print("\nDatos recibidos del sensor:")
    print(datos)

    return jsonify({
        "mensaje": "Datos recibidos correctamente",
        "datos": datos
    }), 200


@app.route("/api/lecturas", methods=["GET"])
def obtener_lecturas():
    return jsonify({
        "cantidad": len(lecturas),
        "lecturas": lecturas
    }), 200

# ==========================================
# PRUEBA DE CONEXION CON SQLITE
# ==========================================

@app.route("/api/db-test", methods=["GET"])
def probar_base_datos():

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tablas = [fila["name"] for fila in cursor.fetchall()]

        conexion.close()

        return jsonify({
            "ok": True,
            "base_datos": DB_PATH,
            "tablas": tablas,
            "mensaje": "Conexion con SQLite correcta"
        }), 200

    except Exception as error:

        return jsonify({
            "ok": False,
            "mensaje": "Error al conectar con SQLite",
            "error": str(error)
        }), 500


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

