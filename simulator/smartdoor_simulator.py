# ============================================================
# SmartDoor - Simulador IoT de sensor de puerta
# ============================================================

import json
import random
import time
import requests
from datetime import datetime, timezone
from pathlib import Path


# ============================================================
# 1. CARGAR CONFIGURACION DESDE config.json
# ============================================================

RUTA_CONFIG = Path(__file__).parent / "config.json"

with open(RUTA_CONFIG, "r", encoding="utf-8") as archivo:
    config = json.load(archivo)


device_id = config["device_id"]
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


# ============================================================
# 2. CONFIGURAR SEMILLA ALEATORIA
# ============================================================

random.seed(seed)


# ============================================================
# 3. VARIABLES DEL SIMULADOR
# ============================================================

sequence = 0
access_count = 0

door_state = "CLOSED"
open_duration = 0
open_cycles = 0


# ============================================================
# 4. MOSTRAR CONFIGURACION
# ============================================================

print("=" * 55)
print("        SMARTDOOR - SIMULADOR IoT")
print("=" * 55)

print(f"Dispositivo       : {device_id}")
print(f"Escenario         : {scenario}")
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

def actualizar_sensor():

    global door_state
    global open_duration
    global access_count
    global open_cycles

    estado_anterior = door_state

    # --------------------------------------------------------
    # ESCENARIO NORMAL
    # --------------------------------------------------------

    if scenario == "normal":

        if door_state == "CLOSED":

            if random.random() < open_probability:
                door_state = "OPEN"
                open_duration = 0
                open_cycles = 0

        else:

            open_cycles += 1
            open_duration += interval_seconds

            if open_cycles >= normal_open_cycles:
                door_state = "CLOSED"
                open_duration = 0
                open_cycles = 0

    # --------------------------------------------------------
    # ESCENARIO ALERTA
    # --------------------------------------------------------

    elif scenario == "alert":

        if door_state == "CLOSED":

            door_state = "OPEN"
            open_duration = 0
            open_cycles = 0

        else:

            open_duration += interval_seconds

            if open_duration > max_open_seconds:
                open_duration = max_open_seconds

    # --------------------------------------------------------
    # CONTAR APERTURAS
    # CLOSED -> OPEN
    # --------------------------------------------------------

    if estado_anterior == "CLOSED" and door_state == "OPEN":
        access_count += 1


# ============================================================
# 7. CREAR JSON DE TELEMETRIA
# ============================================================

def crear_telemetria():

    global sequence

    sequence += 1

    if door_state == "OPEN" and open_duration >= alert_after_seconds:
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    message_id = f"{device_id}-{sequence:06d}"

    datos = {

        "message_id": message_id,

        "device_id": device_id,

        "timestamp": obtener_timestamp(),

        "sequence": sequence,

        "measurements": {

            "door_state": door_state,

            "open_duration": open_duration,

            "access_count": access_count,

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
# 9. CICLO PRINCIPAL DEL SIMULADOR
# ============================================================

contador_mensajes = 0

try:

    while True:

        actualizar_sensor()

        datos_sensor = crear_telemetria()

        print("\n" + "=" * 55)
        print(f"LECTURA #{sequence}")
        print("=" * 55)

        print(
            json.dumps(
                datos_sensor,
                indent=4,
                ensure_ascii=False
            )
        )

        enviar_telemetria(datos_sensor)

        contador_mensajes += 1

        # max_messages = 0 significa ejecución continua
        if max_messages > 0 and contador_mensajes >= max_messages:
            print("\nSimulación finalizada.")
            break

        time.sleep(interval_seconds)


except KeyboardInterrupt:

    print("\n\nSimulador detenido por el usuario.")