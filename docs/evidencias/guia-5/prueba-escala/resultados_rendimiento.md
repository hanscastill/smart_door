# Guía 5 - Actividad 9: Pruebas de rendimiento

## Proyecto SmartDoor

### Escenario evaluado
- Dispositivos registrados: 100.
- Endpoint: GET /api/devices.
- Servidor: FastAPI local.
- Consultas realizadas: 5.

### Resultados

| Prueba | HTTP | Tiempo |
|---|---|---|
| 1 | 200 | 7.56 ms |
| 2 | 200 | 6.55 ms |
| 3 | 200 | 6.61 ms |
| 4 | 200 | 8.09 ms |
| 5 | 200 | 6.65 ms |

Tiempo promedio: 7.07 ms.

### Resultado

Las cinco consultas finalizaron correctamente.

Estos tiempos corresponden a pruebas locales y no
representan el rendimiento de un despliegue urbano.

### Conclusión

SmartDoor respondió correctamente a las consultas
realizadas con 100 dispositivos registrados.
