# Decisión de Persistencia - SmartDoor

## Base de datos seleccionada

El proyecto SmartDoor utiliza SQLite como mecanismo de persistencia de datos.

La base de datos principal se encuentra en:

database/smartdoor.db

## Justificación

SQLite fue seleccionada porque permite almacenar la telemetría de los sensores IoT de forma sencilla, local y persistente, sin requerir un servidor de base de datos adicional.

## Información almacenada

SmartDoor almacena información de telemetría como:

- message_id
- device_id
- timestamp
- sequence
- door_state
- open_duration
- access_count
- alert_status

## Integración

Los dispositivos simulados generan telemetría y la transmiten mediante MQTT utilizando el tópico:

smartdoor/telemetry

El backend procesa los mensajes y registra la información en SQLite.

La información almacenada posteriormente puede ser consultada mediante la API REST y utilizada por:

- Dashboard SmartDoor
- Módulo de alertas
- Módulo de reportes
- Gráficas estadísticas

## Decisión

Se mantiene SQLite como mecanismo de persistencia del proyecto debido a su simplicidad, portabilidad y adecuada integración con el backend de SmartDoor.
