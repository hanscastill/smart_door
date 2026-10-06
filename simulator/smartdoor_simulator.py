# ============================================================
# SmartDoor - Simulador IoT de sensor de puerta
# ============================================================

import json
import random
import time
import requests
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# 1. CARGAR CONFIGURACION DESDE config.json
# ============================================================

RUTA_CONFIG = Path(__file__).parent / "config.json"

with open(RUTA_CONFIG, "r", encoding="utf-8") as archivo:
    config = json.load(archivo)


devices = config["devices"]
interval_seconds = config["interval_seconds"]
scenario = config["scenario"]
seed = config["seed"]
http_url = config["http_url"]
http_retries = config["http_retries"]
max_messages = config["max_messages"]
open_probability = config["open_probability"]
normal_open_cycles = config["normal_open_cycles"]
alert_after_seconds = config["alert_after_seconds"]
max_open_seconds = config["max_open_seconds"]
transport = config.get("transport", "both").lower()

# ============================================================
# CONFIGURACION MQTT
# ============================================================

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "smartdoor/telemetry"

cliente_mqtt = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

try:
    cliente_mqtt.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    cliente_mqtt.loop_start()

    print(
        f"MQTT conectado a "
        f"{MQTT_BROKER}:{MQTT_PORT}"
    )

except Exception as error:
    print(
        f"Error conectando con MQTT: {error}"
    )


# ============================================================
# 2. CONFIGURAR SEMILLA ALEATORIA
# ============================================================

random.seed(seed)


# ============================================================
# 3. VARIABLES DEL SIMULADOR
# ============================================================

# Estado independiente para cada dispositivo SmartDoor
# Estado independiente para cada dispositivo SmartDoor
estados_dispositivos = {}


def obtener_ultima_secuencia(device_id):
    """
    Consulta al backend la última secuencia registrada
    para evitar message_id duplicados.
    """

    try:
        url = f"http://127.0.0.1:8000/api/devices/{device_id}/telemetry"

        respuesta = requests.get(
            url,
            timeout=5
        )

        if respuesta.status_code == 200:

            datos = respuesta.json()
            telemetria = datos.get("telemetry", [])

            if telemetria:
                return int(telemetria[0]["sequence"])

    except requests.exceptions.RequestException as error:
        print(
            f"No se pudo consultar la secuencia de "
            f"{device_id}: {error}"
        )

    return 0


for dispositivo in devices:

    ultima_secuencia = obtener_ultima_secuencia(dispositivo)

    estados_dispositivos[dispositivo] = {
        "sequence": ultima_secuencia,
        "access_count": 0,
        "door_state": "CLOSED",
        "open_duration": 0,
        "open_cycles": 0
    }

    print(
        f"{dispositivo} inicia desde sequence "
        f"{ultima_secuencia}"
    )
print("=" * 55)
print("        SMARTDOOR - SIMULADOR IoT")
print("=" * 55)

print("Dispositivos     :")
for dispositivo in devices:
    print(f"  - {dispositivo}")

print(f"Total dispositivos: {len(devices)}")
print(f"Escenario         : {scenario}")
print(f"Intervalo         : {interval_seconds} segundos")
print(f"API               : {http_url}")
print(f"Alerta después de : {alert_after_seconds} segundos")

print("=" * 55)
print(f"Intervalo         : {interval_seconds} segundos")
print(f"API               : {http_url}")
print(f"Alerta después de : {alert_after_seconds} segundos")

print("=" * 55)


# ============================================================
# 5. FUNCION PARA CREAR TIMESTAMP UTC
# ============================================================

def obtener_timestamp():

    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


# ============================================================
# 6. FUNCION PARA ACTUALIZAR EL ESTADO DE LA PUERTA
# ============================================================

def actualizar_sensor(device_id):

    estado = estados_dispositivos[device_id]

    estado_anterior = estado["door_state"]

    # ---------------------------------------------
    # ESCENARIO NORMAL
    # ---------------------------------------------

    if scenario == "normal":

        if estado["door_state"] == "CLOSED":

            if random.random() < open_probability:
                estado["door_state"] = "OPEN"
                estado["open_duration"] = 0
                estado["open_cycles"] = 0

        else:

            estado["open_cycles"] += 1
            estado["open_duration"] += interval_seconds

            if estado["open_cycles"] >= normal_open_cycles:
                estado["door_state"] = "CLOSED"
                estado["open_duration"] = 0
                estado["open_cycles"] = 0

    # ---------------------------------------------
    # ESCENARIO ALERTA
    # ---------------------------------------------

    elif scenario == "alert":

        # DOOR-002 permanece cerrada para simular
        # una puerta funcionando en estado normal.
        if device_id == "DOOR-002":
            estado["door_state"] = "CLOSED"
            estado["open_duration"] = 0
            estado["open_cycles"] = 0

        # DOOR-001 y DOOR-003 simulan apertura prolongada.
        else:
            if estado["door_state"] == "CLOSED":
                estado["door_state"] = "OPEN"
                estado["open_duration"] = 0
                estado["open_cycles"] = 0

            else:
                estado["open_duration"] += interval_seconds

                if estado["open_duration"] > max_open_seconds:
                    estado["open_duration"] = max_open_seconds

    # ---------------------------------------------
    # CONTAR APERTURAS
    # CLOSED -> OPEN
    # ---------------------------------------------

    if (
        estado_anterior == "CLOSED"
        and estado["door_state"] == "OPEN"
    ):
        estado["access_count"] += 1


# ============================================================
# 7. CREAR JSON DE TELEMETRIA
# ============================================================

def crear_telemetria(device_id):

    estado = estados_dispositivos[device_id]

    # Incrementar secuencia independiente del dispositivo
    estado["sequence"] += 1

    # Determinar estado de alerta
    if (
        estado["door_state"] == "OPEN"
        and estado["open_duration"] >= alert_after_seconds
    ):
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    # ID único por dispositivo y secuencia
    message_id = f"{device_id}-{estado['sequence']:06d}"

    datos = {
        "message_id": message_id,
        "device_id": device_id,
        "timestamp": obtener_timestamp(),
        "sequence": estado["sequence"],
        "measurements": {
            "door_state": estado["door_state"],
            "open_duration": estado["open_duration"],
            "access_count": estado["access_count"],
            "alert_status": alert_status
        }
    }

    return datos


# ============================================================
# 8. ENVIAR JSON AL BACKEND
# ============================================================

def enviar_telemetria(datos):

    for intento in range(1, http_retries + 1):

        try:

            respuesta = requests.post(
                http_url,
                json=datos,
                timeout=5
            )

            print("\nRespuesta del backend:")
            print("Código HTTP:", respuesta.status_code)

            try:
                print(
                    json.dumps(
                        respuesta.json(),
                        indent=4,
                        ensure_ascii=False
                    )
                )

            except ValueError:
                print(respuesta.text)

            return

        except requests.exceptions.RequestException as error:

            print(
                f"Intento {intento}/{http_retries} fallido:"
            )

            print(error)

            if intento < http_retries:
                time.sleep(2)


# ============================================================
# 9. PUBLICAR TELEMETRIA POR MQTT
# ============================================================

def publicar_mqtt(datos):

    try:

        mensaje = json.dumps(
            datos,
            ensure_ascii=False
        )

        resultado = cliente_mqtt.publish(
            MQTT_TOPIC,
            mensaje
        )

        resultado.wait_for_publish()

        print(
            f"MQTT publicado correctamente: "
            f"{datos['device_id']} -> {MQTT_TOPIC}"
        )

    except Exception as error:

        print(
            f"Error publicando MQTT: {error}"
        )


# ============================================================
# 9. CICLO PRINCIPAL DEL SIMULADOR
# ============================================================

contador_mensajes = 0

try:

    while True:

        # Recorrer todos los dispositivos configurados
        for device_id in devices:

            # Actualizar estado independiente del dispositivo
            actualizar_sensor(device_id)

            # Crear telemetría del dispositivo
            datos_sensor = crear_telemetria(device_id)

            estado = estados_dispositivos[device_id]

            print("\n" + "=" * 55)
            print(
                f"DISPOSITIVO: {device_id} | "
                f"LECTURA #{estado['sequence']}"
            )
            print("=" * 55)

            print(
                json.dumps(
                    datos_sensor,
                    indent=4,
                    ensure_ascii=False
                )
            )

            # Seleccionar transporte de telemetría
            if transport == "http":
                enviar_telemetria(datos_sensor)

            elif transport == "mqtt":
                publicar_mqtt(datos_sensor)

            elif transport == "both":
                enviar_telemetria(datos_sensor)
                publicar_mqtt(datos_sensor)

            else:
                print(
                    f"Transport no válido: {transport}. "
                    "Use http, mqtt o both."
                )
            

            contador_mensajes += 1

            # max_messages = 0 significa ejecución continua
            if (
                max_messages > 0
                and contador_mensajes >= max_messages
            ):
                break

        if max_messages > 0 and contador_mensajes >= max_messages:
            print("\nSimulación finalizada.")
            break

        time.sleep(interval_seconds)


except KeyboardInterrupt:

    print("\n\nSimulador detenido por el usuario.")