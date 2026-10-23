# Evidencia A5 - Historicos y rango temporal

## Proyecto SmartDoor

### 1. Necesidad historica

Consultar las ultimas cinco lecturas del sensor de puerta DOOR-001 durante un periodo determinado, para analizar su estado de apertura y las alertas registradas.

### 2. URL REST diseñada

GET /api/measurements?device_id=DOOR-001&limit=5&from=2026-10-01T00:00:00Z&to=2026-10-23T23:59:59Z

### 3. Parametros utilizados

- device_id: identifica el dispositivo.
- limit: cantidad maxima de registros.
- offset: desplazamiento de registros, por defecto 0.
- from: fecha inicial del periodo.
- to: fecha final del periodo.

Las fechas se expresan en UTC.

### 4. Respuesta obtenida

- Codigo HTTP: 200 OK.
- Estado: success.
- Dispositivo: DOOR-001.
- Registros devueltos: 5.
- Periodo: 1 al 23 de octubre de 2026.
- Se observaron estados OPEN y alertas NORMAL y ALERT.

### 5. Evidencia

A5_01_consulta_historica_200.png

### 6. Utilidad para el dashboard

Permite consultar el historial de un dispositivo sin recuperar toda la base de datos.

Facilita el analisis de aperturas, duracion de eventos y alertas dentro de un periodo seleccionado.

### 7. Conclusion

Se implemento y comprobo una consulta REST con filtros por dispositivo, limite de registros y rango temporal.

La API respondio correctamente y devolvio cinco mediciones correspondientes al intervalo solicitado.
