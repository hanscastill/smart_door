# SmartDoor - Simulador IoT de sensor de puerta

import random
import json
from datetime import datetime, timezone

print("================================")
print("   SMARTDOOR - SENSOR DE PUERTA")
print("================================")

# Simular el estado del sensor magnético
door_state = random.choice(["ABIERTA", "CERRADA"])

# Simular el tiempo que la puerta permanece abierta
if door_state == "ABIERTA":
    open_duration = random.randint(1, 120)
else:
    open_duration = 0

# Simular la cantidad de aperturas de la puerta
access_count = random.randint(0, 20)

# Mostrar los datos simulados
print("Estado de la puerta:", door_state)
print("Tiempo abierta:", open_duration, "segundos")
print("Cantidad de aperturas:", access_count)

# Crear los datos del sensor en formato JSON
datos_sensor = {
    "device_id": "SMARTDOOR-001",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "measurements": {
        "door_state": door_state,
        "open_duration": open_duration,
        "access_count": access_count
    }
}

print("\nDatos JSON:")
print(json.dumps(datos_sensor, indent=4))