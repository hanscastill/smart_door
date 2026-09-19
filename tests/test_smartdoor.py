def test_door_state_valido():
    estados_validos = ["OPEN", "CLOSED"]
    door_state = "OPEN"

    assert door_state in estados_validos


def test_open_duration_no_negativo():
    open_duration = 30

    assert open_duration >= 0


def test_access_count_no_negativo():
    access_count = 1

    assert access_count >= 0


def test_alert_status_normal():
    door_state = "OPEN"
    open_duration = 15
    alert_after_seconds = 30

    if door_state == "OPEN" and open_duration >= alert_after_seconds:
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    assert alert_status == "NORMAL"


def test_alert_status_alert():
    door_state = "OPEN"
    open_duration = 30
    alert_after_seconds = 30

    if door_state == "OPEN" and open_duration >= alert_after_seconds:
        alert_status = "ALERT"
    else:
        alert_status = "NORMAL"

    assert alert_status == "ALERT"


def test_estructura_json_telemetria():
    telemetria = {
        "message_id": "DOOR-001-000001",
        "device_id": "DOOR-001",
        "timestamp": "2026-09-19T05:52:04Z",
        "sequence": 1,
        "measurements": {
            "door_state": "OPEN",
            "open_duration": 30,
            "access_count": 1,
            "alert_status": "ALERT"
        }
    }

    assert "message_id" in telemetria
    assert "device_id" in telemetria
    assert "timestamp" in telemetria
    assert "sequence" in telemetria
    assert "measurements" in telemetria