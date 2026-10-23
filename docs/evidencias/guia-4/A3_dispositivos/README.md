# Evidencia A3 - Dispositivos SmartDoor

## Dispositivo existente
GET /api/devices/DOOR-001

Resultado: HTTP 200 OK.

## Dispositivo inexistente
GET /api/devices/DOOR-999

Resultado: HTTP 404 Not Found.

## Explicación
Cuando se consulta un device_id inexistente, la API devuelve HTTP 404 porque el recurso solicitado no fue encontrado.
El código HTTP 200 se utiliza cuando el dispositivo existe y la consulta se realiza correctamente.
Esta diferencia permite identificar los recursos disponibles y manejar adecuadamente los errores de consulta.

## Evidencias
- A3_01_dispositivo_existente_200.png
- A3_02_dispositivo_inexistente_404.png
