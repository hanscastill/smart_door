
# ACTIVIDAD 4. DISEÑAR ANTES DE CODIFICAR

## Proyecto SmartDoor - Sistema IoT

### 1. Objetivo

Diseñar un panel web para consultar y monitorear
dispositivos IoT de puertas, visualizar sus estados,
consultar mediciones históricas e identificar alertas.

El frontend obtendrá la información mediante
la API REST desarrollada con FastAPI.

## 2. Wireframe del panel de monitoreo

```text
+------------------------------------------------------+
|             SMARTDOOR - PANEL IoT                    |
+------------------------------------------------------+
| Seleccionar dispositivo: [ DOOR-001          v ]     |
| Endpoint: GET /api/devices                           |
+--------------------------+---------------------------+
| DISPOSITIVOS             | ESTADO DE PUERTA          |
| Total registrados        | OPEN / CLOSED             |
| GET /api/devices         | GET /api/measurements     |
+--------------------------+---------------------------+
| ACCESOS ACUMULADOS       | TIEMPO DE APERTURA        |
| access_count             | open_duration (segundos)  |
| GET /api/measurements    | GET /api/measurements     |
+--------------------------+---------------------------+
| GRÁFICA 1: TIEMPO DE APERTURA                        |
| Eje X: timestamp                                     |
| Eje Y: open_duration                                 |
| GET /api/measurements                                |
+------------------------------------------------------+
| GRÁFICA 2: ACCESOS HISTÓRICOS                        |
| Eje X: timestamp                                     |
| Eje Y: access_count                                  |
| GET /api/measurements                                |
+------------------------------------------------------+
| TABLA DE MEDICIONES                                  |
| Fecha | Dispositivo | Estado | Duración | Alerta     |
| GET /api/measurements                                |
+------------------------------------------------------+
| MENSAJES DE ESTADO                                   |
| Conectado / Cargando / Sin datos / Error             |
+------------------------------------------------------+
```

## 3. Componentes visuales y endpoints

| Componente | Información | Endpoint |
|---|---|---|
| Tarjeta dispositivos | Total registrado | GET /api/devices |
| Selector de dispositivo | ID y nombre | GET /api/devices |
| Estado de puerta | OPEN / CLOSED | GET /api/measurements |
| Tarjeta de accesos | access_count | GET /api/measurements |
| Tiempo de apertura | open_duration | GET /api/measurements |
| Gráfica 1 | timestamp y open_duration | GET /api/measurements |
| Gráfica 2 | timestamp y access_count | GET /api/measurements |
| Tabla de mediciones | Historial y alertas | GET /api/measurements |
| Mensajes de estado | Resultado de la consulta | Respuesta HTTP |

## 4. Arquitectura de comunicación

El frontend no consultará directamente SQLite.

Flujo de información:

Usuario
   |
   v
Frontend HTML, CSS y JavaScript
   |
   | Petición HTTP GET
   v
Backend FastAPI
   |
   | Consulta a SQLite
   v
Base de datos
   |
   v
Backend devuelve JSON
   |
   v
Frontend muestra los resultados

## 5. Variables numéricas históricas

### Variable 1: open_duration

Representa el tiempo de apertura de una puerta,
expresado en segundos.

Se utilizará en una gráfica histórica donde:

- Eje X: timestamp.
- Eje Y: open_duration.

### Variable 2: access_count

Representa el conteo acumulado de accesos
registrados por un dispositivo.

Se utilizará en otra gráfica histórica donde:

- Eje X: timestamp.
- Eje Y: access_count.

Ambas variables permiten observar cambios
a lo largo del tiempo.

## 6. Mensajes de estado

- Cargando: consulta en proceso.
- Conectado: respuesta HTTP exitosa.
- Sin datos: no existen mediciones disponibles.
- Error: fallo al consultar la API.
- Alerta: medición con estado ALERT.

## 7. Validación de los requisitos

1. Wireframe del panel: Diseñado.
2. Tarjetas, tablas, gráficas y selector: Identificados.
3. Endpoints asociados: Documentados.
4. Acceso directo del frontend a SQLite: No permitido.
5. Dos variables numéricas históricas: Definidas.

## 8. Conclusión

Se diseñó un panel de monitoreo IoT para SmartDoor,
identificando los componentes visuales y su relación
con los endpoints de la API REST.

La arquitectura mantiene separados el frontend,
el backend FastAPI y la base de datos SQLite.

El diseño permitirá implementar posteriormente
las tarjetas, gráficas, tablas y mensajes de estado.

Nota: Se verificará la estructura real del endpoint
GET /api/measurements antes de implementar las gráficas.
