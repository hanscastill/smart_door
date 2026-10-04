devices = config["devices"]
# Estado independiente para cada dispositivo SmartDoor
estados_dispositivos = {}

for dispositivo in devices:
    estados_dispositivos[dispositivo] = {
        "sequence": 0,
        "access_count": 0,
        "door_state": "CLOSED",
        "open_duration": 0,
        "open_cycles": 0
    }