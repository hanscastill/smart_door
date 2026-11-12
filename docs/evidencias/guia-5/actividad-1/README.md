# Guía 5 - Actividad 1
## Verificación de la API REST SmartDoor

### Objetivo
Comprobar el funcionamiento de los endpoints de
dispositivos, telemetría y alertas antes de continuar
con la integración del dashboard.

### Pruebas realizadas

| Endpoint | Resultado |
|---|---|
| GET /api/devices | 200 OK |
| GET /api/devices/DOOR-001/latest | 200 OK |
| GET /api/devices/DOOR-001/telemetry | 200 OK |
| GET /api/alertas | 200 OK |

### Evidencias
- checkpoint_api.json
- Capturas de Swagger UI
- Verificación de respuestas HTTP 200

### Conclusión
Los cuatro endpoints evaluados respondieron
correctamente y devolvieron información JSON.

La API REST está disponible para continuar
con las siguientes pruebas de integración.
