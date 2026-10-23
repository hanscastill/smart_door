# Evidencia A4 - Fase 4: Filtros y paginación

## Proyecto SmartDoor

### Objetivo
Implementar filtros, parámetros de consulta y paginación básica en la API REST desarrollada con FastAPI y SQLite.

## Pruebas realizadas

| Prueba | URL | HTTP | Registros |
|---|---|---|---|
| Limit 5 | /api/measurements?limit=5 | 200 | 5 |
| Offset 5 | /api/measurements?limit=5&offset=5 | 200 | 5 |
| Filtro por dispositivo | /api/measurements?device_id=DOOR-001&limit=5 | 200 | 5 |
| Validación limit 500 | /api/measurements?limit=500 | 422 | No aplica |

## Evidencias

- A4_01_limit_5.png
- A4_02_offset_5.png
- A4_03_filtro_device_id.png
- A4_04_validacion_422.png

## Resultados

1. El parámetro limit controla la cantidad máxima de registros.
2. El parámetro offset permite omitir registros para realizar paginación.
3. El parámetro device_id permite consultar las mediciones de un dispositivo específico.
4. FastAPI rechaza valores superiores a 100 mediante HTTP 422.

## Conclusión

La Fase 4 permitió implementar consultas controladas mediante filtros y paginación. Las pruebas demostraron que la API REST puede limitar los registros, desplazarse entre resultados y consultar mediciones específicas.

Además, la validación de FastAPI evita solicitudes que superen el límite permitido de 100 registros, contribuyendo al control de las consultas sobre SQLite.
