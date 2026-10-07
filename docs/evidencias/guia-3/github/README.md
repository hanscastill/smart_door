# Evidencia Git y GitHub - SmartDoor

## Objetivo

Documentar el uso de Git y GitHub para el control de versiones del proyecto SmartDoor.

## Repositorio

SmartDoor utiliza Git como sistema de control de versiones y GitHub como repositorio remoto.

La rama principal utilizada es:

`main`

## Flujo de trabajo

Durante el desarrollo se utilizaron comandos como:

`git status`

`git add`

`git commit`

`git push origin main`

`git log`

Estos comandos permiten controlar los cambios realizados y mantener actualizado el repositorio remoto.

## Historial de desarrollo

El historial de commits evidencia la evolución progresiva del proyecto, incluyendo:

- Simulador inicial SmartDoor.
- Backend y API.
- Persistencia SQLite.
- Dashboard.
- Alertas.
- Reportes.
- Gráficas.
- Arquitectura.
- MQTT.
- Pruebas automáticas.
- Documentación.

## Integración MQTT

El repositorio contiene la implementación del flujo:

Dispositivos IoT → MQTT → Mosquitto → FastAPI → SQLite

También conserva la API REST para consultas y operaciones del sistema.

## Estado del repositorio

Antes de cada publicación se utiliza:

`git status`

Después se registran los cambios mediante un commit y finalmente se sincronizan con GitHub utilizando:

`git push origin main`

## Resultado

Git y GitHub permiten mantener trazabilidad sobre la evolución de SmartDoor y conservar de forma organizada el código fuente y la documentación técnica.
