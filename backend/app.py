from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import threading
import json
import paho.mqtt.client as mqtt


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
# ==========================================================
# API DE REPORTES SMARTDOOR
# GET /api/reportes
# ==========================================================

@app.route("/api/reportes", methods=["GET"])
def obtener_reportes():
    conexion = obtener_conexion()

    try:
        total_lecturas = conexion.execute(
            "SELECT COUNT(*) AS total FROM telemetry"
        ).fetchone()["total"]

        total_alertas = conexion.execute(
            "SELECT COUNT(*) AS total FROM telemetry "
            "WHERE alert_status = 'ALERT'"
        ).fetchone()["total"]

        total_normal = conexion.execute(
            "SELECT COUNT(*) AS total FROM telemetry "
            "WHERE alert_status = 'NORMAL'"
        ).fetchone()["total"]

        tiempo_promedio = conexion.execute(
            "SELECT ROUND(AVG(open_duration), 2) AS promedio "
            "FROM telemetry"
        ).fetchone()["promedio"]

        tiempo_maximo = conexion.execute(
            "SELECT MAX(open_duration) AS maximo FROM telemetry"
        ).fetchone()["maximo"]

        total_accesos = conexion.execute(
            "SELECT SUM(access_count) AS total FROM telemetry"
        ).fetchone()["total"]

        return jsonify({
            "status": "success",
            "reporte": {
                "total_lecturas": total_lecturas,
                "total_alertas": total_alertas,
                "total_normal": total_normal,
                "tiempo_promedio_abierta": tiempo_promedio or 0,
                "tiempo_maximo_abierta": tiempo_maximo or 0,
                "total_accesos": total_accesos or 0
            }
        }), 200

    except sqlite3.Error as error:
        return jsonify({
            "status": "error",
            "message": "Error consultando reportes en SQLite",
            "error": str(error)
        }), 500

    finally:
        conexion.close()
lecturas = []
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ==========================================================
# PAGINA DE REPORTES
# ==========================================================

@app.route("/reportes")
def reportes():
    return render_template("reportes.html")
# =====================================================
# PAGINA DE ALERTAS
# =====================================================

@app.route("/alertas")
def pagina_alertas():
    return render_template("alertas.html")


# ==========================================================
# API - ALERTAS DE SMARTDOOR
# ==========================================================

@app.route("/api/alertas", methods=["GET"])
def obtener_alertas():
    conexion = obtener_conexion()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id,
                device_id,
                timestamp,
                door_state,
                open_duration,
                access_count,
                alert_status,
                message_id,
                sequence
            FROM telemetry
            WHERE alert_status = 'ALERT'
            ORDER BY id DESC
        """)

        filas = cursor.fetchall()

        alertas = []

        for fila in filas:
            alertas.append({
                "id": fila["id"],
                "device_id": fila["device_id"],
                "timestamp": fila["timestamp"],
                "door_state": fila["door_state"],
                "open_duration": fila["open_duration"],
                "access_count": fila["access_count"],
                "alert_status": fila["alert_status"],
                "message_id": fila["message_id"],
                "sequence": fila["sequence"]
            })

        return jsonify({
            "status": "success",
            "cantidad": len(alertas),
            "alertas": alertas
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:
        conexion.close()


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

    # --------------------------------------------------
    # Validar tipos de datos
    # --------------------------------------------------

    if not isinstance(datos["sequence"], int):
        return jsonify({
            "status": "error",
            "message": "Tipo de dato invalido",
            "field": "sequence",
            "expected": "integer"
        }), 400

    if not isinstance(measurements["open_duration"], (int, float)):
        return jsonify({
            "status": "error",
            "message": "Tipo de dato invalido",
            "field": "open_duration",
            "expected": "number"
        }), 400

    if not isinstance(measurements["access_count"], int):
        return jsonify({
            "status": "error",
            "message": "Tipo de dato invalido",
            "field": "access_count",
            "expected": "integer"
        }), 400

    if not isinstance(measurements["door_state"], str):
        return jsonify({
            "status": "error",
            "message": "Tipo de dato invalido",
            "field": "door_state",
            "expected": "string"
        }), 400

        # --------------------------------------------------
    # Validar reglas de negocio de SmartDoor
    # --------------------------------------------------

    if measurements["door_state"] not in ["OPEN", "CLOSED"]:
        return jsonify({
            "status": "error",
            "message": "Estado de puerta invalido",
            "field": "door_state",
            "expected": "OPEN o CLOSED"
        }), 400

    if measurements["door_state"] == "CLOSED" and measurements["open_duration"] != 0:
        return jsonify({
            "status": "error",
            "message": "Una puerta CLOSED debe tener open_duration igual a 0",
            "field": "open_duration",
            "expected": 0
        }), 400

    door_state = measurements["door_state"]
    open_duration = measurements["open_duration"]
    access_count = measurements["access_count"]

    if door_state == "OPEN" and open_duration > 30:
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    measurements["alert_status"] = alert_status

    # -------------------------------------------------------
    # Guardar temporalmente la lectura
    # -------------------------------------------------------
    lecturas.append(datos)

    # =======================================================
    # GUARDAR TELEMETRIA EN SQLITE
    # =======================================================

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

    conexion = obtener_conexion()

    try:
        registros = conexion.execute("""
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
            ORDER BY id DESC
        """).fetchall()

        lecturas_db = []

        for registro in registros:

            lectura = {
                "message_id": registro["message_id"],
                "device_id": registro["device_id"],
                "timestamp": registro["timestamp"],
                "sequence": registro["sequence"],

                "measurements": {
                    "door_state": registro["door_state"],
                    "open_duration": registro["open_duration"],
                    "access_count": registro["access_count"],
                    "alert_status": registro["alert_status"]
                }
            }

            lecturas_db.append(lectura)

        return jsonify({
            "cantidad": len(lecturas_db),
            "lecturas": lecturas_db
        }), 200

    except sqlite3.Error as error:

        return jsonify({
            "status": "error",
            "message": "Error consultando lecturas en SQLite",
            "error": str(error)
        }), 500

    finally:
        conexion.close()

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

# ==================================================
# CONFIGURACION MQTT SMARTDOOR
# ==================================================

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "smartdoor/telemetry"


def on_mqtt_connect(client, userdata, flags, reason_code, properties):
    print("=== MQTT SMARTDOOR ===")

    if reason_code == 0:
        print("Conectado correctamente al broker MQTT")
        print("Broker:", MQTT_BROKER)
        print("Puerto:", MQTT_PORT)
        print("Topic:", MQTT_TOPIC)

        client.subscribe(MQTT_TOPIC)

        print("Suscripcion MQTT realizada correctamente")
    else:
        print("Error conectando al broker MQTT:", reason_code)


def on_mqtt_message(client, userdata, msg):

    print("\n==============================================")
    print("NUEVA TELEMETRIA RECIBIDA POR MQTT")
    print("==============================================")

    try:
        payload = msg.payload.decode("utf-8")
        datos = json.loads(payload)

        print("Topic:", msg.topic)
        print("Payload:", datos)

        # ------------------------------------------
        # Validar campos principales
        # ------------------------------------------

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
            campo
            for campo in campos_medicion
            if campo not in measurements
        ]

        if faltantes_medicion:
            print(
                "ERROR MQTT - Faltan campos en measurements:",
                faltantes_medicion
            )
            return

        # ------------------------------------------
        # Validar tipos
        # ------------------------------------------

        if not isinstance(datos["sequence"], int):
            print("ERROR MQTT - sequence debe ser integer")
            return

        if not isinstance(
            measurements["open_duration"],
            (int, float)
        ):
            print("ERROR MQTT - open_duration debe ser numerico")
            return

        if not isinstance(measurements["access_count"], int):
            print("ERROR MQTT - access_count debe ser integer")
            return

        if not isinstance(measurements["door_state"], str):
            print("ERROR MQTT - door_state debe ser string")
            return

        # ------------------------------------------
        # Reglas SmartDoor
        # ------------------------------------------

        door_state = measurements["door_state"]
        open_duration = measurements["open_duration"]
        access_count = measurements["access_count"]

        if door_state not in ["OPEN", "CLOSED"]:
            print("ERROR MQTT - door_state invalido")
            return

        if door_state == "CLOSED" and open_duration != 0:
            print(
                "ERROR MQTT - Una puerta CLOSED "
                "debe tener open_duration = 0"
            )
            return

        # ------------------------------------------
        # Calcular alerta
        # ------------------------------------------

        if door_state == "OPEN" and open_duration > 30:
            alert_status = "ALERT"
        else:
            alert_status = "NORMAL"

        # ------------------------------------------
        # Guardar en SQLite
        # ------------------------------------------

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
        conexion.close()

        print("----------------------------------------------")
        print("TELEMETRIA MQTT GUARDADA EN SQLITE")
        print("Message ID:", datos["message_id"])
        print("Device ID:", datos["device_id"])
        print("Estado:", door_state)
        print("Tiempo abierta:", open_duration)
        print("Accesos:", access_count)
        print("Alerta:", alert_status)
        print("----------------------------------------------")

    except sqlite3.IntegrityError as error:
        print("MQTT - Message ID duplicado:", error)

    except json.JSONDecodeError as error:
        print("MQTT - JSON invalido:", error)

    except Exception as error:
        print("ERROR procesando MQTT:", error)


def iniciar_mqtt():

    print("Iniciando cliente MQTT SmartDoor...")

    cliente = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="smartdoor-backend"
    )

    cliente.on_connect = on_mqtt_connect
    cliente.on_message = on_mqtt_message

    cliente.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    cliente.loop_forever()
# ==========================================
# INICIAR SERVIDOR
# ==========================================
if __name__ == "__main__":

    print("==============================================")
    print("INICIANDO SMARTDOOR BACKEND")
    print("==============================================")

    # Iniciar MQTT en segundo plano
    hilo_mqtt = threading.Thread(
        target=iniciar_mqtt,
        daemon=True
    )

    hilo_mqtt.start()

    print("Cliente MQTT iniciado en segundo plano")

    # Iniciar servidor Flask
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )