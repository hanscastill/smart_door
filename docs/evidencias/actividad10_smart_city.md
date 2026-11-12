
# ACTIVIDAD 10 - SMARTDOOR EN UN ESCENARIO SMART CITY

## Proyecto: SmartDoor - Sistema IoT

### Objetivo
Analizar cómo la arquitectura del sistema SmartDoor puede ampliarse
para utilizarse en una ciudad inteligente (Smart City).

## 1. Dispositivos en una ciudad inteligente

SmartDoor utiliza sensores IoT para monitorear el estado de las puertas,
registrar tiempos de apertura, contabilizar accesos y generar alertas.

En una ciudad inteligente, estos dispositivos podrían instalarse en:

- Universidades: control de puertas de aulas y laboratorios.
- Hospitales: supervisión de accesos a áreas restringidas.
- Estaciones de transporte: monitoreo de puertas de acceso.
- Edificios públicos: detección de puertas abiertas.
- Centros comerciales: supervisión de accesos y salidas.

## 2. Escalabilidad del sistema

El proyecto SmartDoor fue probado con 100 dispositivos simulados.

Escenarios de ampliación:

- 10 dispositivos: edificio pequeño.
- 100 dispositivos: campus universitario.
- 1.000 dispositivos: diferentes edificios de una ciudad.
- 10.000 dispositivos: infraestructura urbana distribuida.

Las cantidades superiores a 100 son escenarios propuestos
y no representan pruebas de rendimiento realizadas.

## 3. Usuarios del dashboard

El dashboard podría ser utilizado por:

- Operadores de seguridad.
- Administradores de edificios.
- Personal de mantenimiento.
- Responsables de infraestructura urbana.

Estos usuarios podrían consultar estados de puertas,
historiales de apertura y alertas de seguridad.

## 4. Decisiones operativas

Ejemplo:

Un sensor detecta que una puerta permanece abierta durante
135 segundos y genera una alerta.

El operador consulta el historial desde el dashboard
y solicita una inspección del acceso.

De esta manera, SmartDoor permite apoyar decisiones
preventivas mediante datos y alertas.

## 5. Tecnologías que deberían evolucionar

Tecnologías actuales:

- Python para el simulador IoT.
- FastAPI para los servicios REST.
- SQLite para almacenar información.
- HTTP y MQTT para comunicación.
- Dashboard web para visualizar datos.

Posibles mejoras para Smart City:

- PostgreSQL para mayor concurrencia y almacenamiento.
- Servidores distribuidos y balanceo de carga.
- Infraestructura MQTT escalable.
- Autenticación y control de acceso.
- Monitoreo centralizado de dispositivos.
- Despliegue en infraestructura de nube.

## Conclusión

SmartDoor demuestra cómo un sistema IoT puede recopilar
telemetría, almacenar registros y presentar información
mediante una aplicación web.

La arquitectura utilizada puede adaptarse a una ciudad
inteligente, pero sería necesario fortalecer la
infraestructura, seguridad y capacidad de procesamiento
para trabajar con miles de dispositivos.

La actividad permite diferenciar los componentes
arquitectónicos reutilizables de las tecnologías
que necesitan evolucionar al aumentar la escala.

## Evidencias del proyecto

- Simulación de 100 dispositivos.
- Registro de telemetría mediante API REST.
- Consulta de dispositivos y lecturas.
- Dashboard con estados, históricos y alertas.
- Pruebas de rendimiento de la Actividad 9.

Actividad 10 - Análisis formativo.
