# Fase 7 - Integración completa de SmartDoor

## 1. Objetivo

Comprobar el recorrido completo de una lectura desde el
simulador hasta su almacenamiento en SQLite y su posterior
recuperación mediante la API REST.

## 2. Identificación de la lectura

- Dispositivo: DOOR-003
- message_id: DOOR-003-099536
- sequence: 99536
- timestamp: 2026-10-25T04:32:46.489233Z
- door_state: OPEN
- open_duration: 30
- access_count: 1

## 3. Matriz de trazabilidad

| Punto de observación | Resultado | Evidencia |
|---|---|---|
| Simulador | Lectura 99536 generada | A7_01 |
| POST /api/telemetry | HTTP 201 Created | A7_01 |
| SQLite | Registro encontrado | A7_02 |
| GET /api/measurements | HTTP 200 OK | A7_03 |
| Después del reinicio | Registro recuperado | A7_04 |

## 4. Evidencias

- A7_01_simulador_post_201.png
- A7_02_verificacion_sqlite.png
- A7_03_consulta_get_200.png
- A7_04_persistencia_reinicio.png

## 5. Observación técnica

Se identificó una diferencia en el campo alert_status.

- Simulador: ALERT.
- Respuesta POST: NORMAL.
- SQLite: NORMAL.
- Respuesta GET: NORMAL.

El message_id, device_id y sequence coinciden durante
el recorrido completo.

Se recomienda revisar la regla de cálculo de alert_status
en el backend para determinar la causa de la diferencia.

## 6. Conclusión

La prueba permitió comprobar que una lectura enviada por
el simulador fue recibida mediante HTTP 201, almacenada
en SQLite y recuperada mediante GET HTTP 200.

También se verificó que el registro permaneció disponible
después de reiniciar el backend.

La trazabilidad y persistencia quedaron demostradas.
Queda pendiente revisar la consistencia del campo
alert_status entre el simulador y el backend.


## 7. Corrección y validación de alertas

Durante las pruebas de integración se identificó una
diferencia entre las alertas generadas por el simulador
y las calculadas por el backend.

Se corrigió la condición de alerta en backend/main.py
para que una puerta abierta durante 30 segundos o más
genere el estado ALERT.

Regla implementada:

- OPEN con duración menor a 30 segundos: NORMAL.
- OPEN con duración igual o mayor a 30 segundos: ALERT.

### Resultados de las pruebas

| Message ID | Duración | Alerta |
|---|---|---|
| DOOR-001-099537 | 15 segundos | NORMAL |
| DOOR-001-099538 | 30 segundos | ALERT |
| DOOR-001-099539 | 45 segundos | ALERT |

La consulta GET /api/measurements confirmó que
las lecturas se recuperan con el estado esperado.

### Evidencias adicionales

- A7_05_correccion_regla_alerta.png
- A7_06_verificacion_alerta_corregida.png

### Conclusión

Se verificó la trazabilidad de las lecturas desde
el simulador hasta la API REST y SQLite.

También se comprobó la persistencia de los registros
después de reiniciar el backend.

La corrección permitió unificar la regla de alertas
entre el simulador y el backend para las lecturas
verificadas.
