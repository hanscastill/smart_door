from pydantic import BaseModel, Field
from typing import Literal


# ==================================================
# MODELOS DE DATOS SMARTDOOR
# ==================================================

class Measurements(BaseModel):
    door_state: Literal["OPEN", "CLOSED"]
    open_duration: float = Field(ge=0)
    access_count: int = Field(ge=0)


class TelemetryCreate(BaseModel):
    message_id: str
    device_id: str
    timestamp: str
    sequence: int = Field(ge=0)
    measurements: Measurements


class TelemetryResponse(BaseModel):
    message_id: str
    device_id: str
    timestamp: str
    sequence: int
    door_state: str
    open_duration: float
    access_count: int
    alert_status: str


# ==================================================
# MODELO PARA DISPOSITIVOS SMARTDOOR
# ==================================================

class DeviceCreate(BaseModel):
    device_id: str
    name: str
    location: str
    enabled: bool = True

    # ==================================================
# MODELO PARA ACTUALIZAR DISPOSITIVOS SMARTDOOR
# ==================================================

class DeviceUpdate(BaseModel):
    name: str
    location: str
    enabled: bool = True


# ==================================================
# MODELO DE RESPUESTA DE DISPOSITIVOS SMARTDOOR
# ==================================================

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    name: str
    location: str
    enabled: bool
    created_at: str