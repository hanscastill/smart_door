# Evidencia de Pruebas Automáticas - SmartDoor

## Objetivo

Comprobar mediante pruebas automáticas que las principales reglas de validación de la telemetría SmartDoor funcionan correctamente.

## Herramienta utilizada

Las pruebas automáticas del proyecto se ejecutan mediante:

`Pytest`

Comando utilizado:

`pytest -v`

## Pruebas ejecutadas

Se comprobaron las siguientes reglas:

1. Estado válido de la puerta.
2. Duración de apertura no negativa.
3. Cantidad de accesos no negativa.
4. Estado NORMAL válido.
5. Estado ALERT válido.
6. Estructura JSON de telemetría válida.

## Resultado obtenido

La ejecución de Pytest produjo:

`6 passed`

Esto significa que las seis pruebas automáticas fueron ejecutadas correctamente sin errores.

## Archivos de pruebas

Las pruebas principales se encuentran en:

`tests/test_smartdoor.py`

También se dispone de:

`tests/test_backend.py`

y:

`simulator/tests/test_simulator.py`

## Validaciones comprobadas

Las pruebas permiten verificar aspectos como:

- door_state válido.
- open_duration no negativo.
- access_count no negativo.
- alert_status NORMAL.
- alert_status ALERT.
- estructura correcta del mensaje de telemetría.

## Resultado

Las pruebas automáticas confirman que las reglas principales de validación de SmartDoor funcionan correctamente.

Resultado final:

6 pruebas ejecutadas → 6 pruebas aprobadas.
