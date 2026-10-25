# Actividad 6 - Matriz de pruebas manuales

## Proyecto SmartDoor
Fase 6: Respuestas, errores y Swagger/OpenAPI.

## Objetivo
Verificar las respuestas HTTP de la API REST SmartDoor,
incluyendo consultas exitosas, recursos inexistentes
y validaciones de parámetros.

## Matriz de pruebas

| Caso | Solicitud | Objetivo | Esperado | Obtenido | Resultado |
|---|---|---|---|---|---|
| 1 | GET /api/measurements?limit=5 | Consultar mediciones | 200 | 200 | Cumple |
| 2 | GET /api/measurements?device_id=DOOR-001&limit=5 | Filtrar mediciones por dispositivo | 200 | 200 | Cumple |
| 3 | GET /api/measurements?device_id=DOOR-999&limit=5 | Consultar sin coincidencias | 200 + [] | 200 + [] | Cumple |
| 4 | GET /api/devices | Listar dispositivos | 200 | 200 | Cumple |
| 5 | GET /api/devices/DOOR-001 | Consultar dispositivo existente | 200 | 200 | Cumple |
| 6 | GET /api/devices/DOOR-999 | Consultar dispositivo inexistente | 404 | 404 | Cumple |
| 7 | GET /api/measurements?limit=500 | Validar limite permitido | 422 | 422 | Cumple |

## Verificacion Swagger/OpenAPI

Se verifico la documentacion interactiva en /docs.

El endpoint GET /api/measurements presenta los parametros:
- device_id
- limit
- offset
- from
- to

Se ejecuto una consulta desde Swagger para DOOR-001,
con limit=5, offset=0 y un rango temporal en UTC.

Resultado obtenido:
- HTTP 200 OK.
- Estado success.
- Cinco mediciones devueltas.

## Evidencias

- A6_01_swagger_endpoints.png
- A6_02_swagger_consulta_200.png

## Conclusion

Las siete pruebas manuales obtuvieron los codigos
HTTP esperados. La API diferencia consultas exitosas,
resultados vacios, recursos inexistentes y parametros
invalidos.

Swagger/OpenAPI permite consultar la documentacion
y ejecutar solicitudes directamente desde el navegador.
