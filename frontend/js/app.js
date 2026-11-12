
// ==========================================
// SMARTDOOR - FRONTEND
// ACTIVIDADES 2, 5, 6 Y 7
// ==========================================

const btnConsultar = document.getElementById("btnConsultar");
const resultado = document.getElementById("resultado");
const selectorDispositivo = document.getElementById("selectorDispositivo");
const btnEstadoActual = document.getElementById("btnEstadoActual");
const estadoPuerta = document.getElementById("estadoPuerta");
const tiempoApertura = document.getElementById("tiempoApertura");
const accesos = document.getElementById("accesos");
const estadoAlerta = document.getElementById("estadoAlerta");
const fechaActualizacion = document.getElementById("fechaActualizacion");
const mensajeEstado = document.getElementById("mensajeEstado");

const btnHistorico = document.getElementById("btnHistorico");
const limiteHistorico = document.getElementById("limiteHistorico");
const mensajeHistorico = document.getElementById("mensajeHistorico");
const interpretacionHistorico =
    document.getElementById("interpretacionHistorico");

// Una sola instancia por gráfica.
let graficaApertura = null;
let graficaAccesos = null;

// ==========================================
// ACTIVIDAD 7 - ESTADOS VISIBLES DEL SISTEMA
// ==========================================

const LIMITE_INACTIVIDAD_MINUTOS = 5;

// Mostrar mensajes comprensibles al usuario.
function mostrarMensaje(elemento, tipo, texto) {
    if (!elemento) return;

    const estilos = {
        exito: {
            fondo: "#e8f5e9",
            color: "#1b5e20",
            borde: "#81c784"
        },
        error: {
            fondo: "#ffebee",
            color: "#b71c1c",
            borde: "#ef9a9a"
        },
        advertencia: {
            fondo: "#fff8e1",
            color: "#795548",
            borde: "#ffcc80"
        },
        informacion: {
            fondo: "#e3f2fd",
            color: "#0d47a1",
            borde: "#90caf9"
        }
    };

    const estilo = estilos[tipo] || estilos.informacion;

    elemento.textContent = texto;
    elemento.style.backgroundColor = estilo.fondo;
    elemento.style.color = estilo.color;
    elemento.style.border = `1px solid ${estilo.borde}`;
    elemento.style.padding = "12px";
    elemento.style.borderRadius = "8px";
    elemento.style.marginTop = "12px";
    elemento.setAttribute("role", "status");
    elemento.setAttribute("aria-live", "polite");
}

// ==========================================
// ACTIVIDAD 7 - VALIDACIÓN DE FECHAS
// ==========================================

// Detectar inactividad a partir de la última lectura.
function verificarInactividad(timestamp) {
    const fechaLectura = new Date(timestamp);

    if (Number.isNaN(fechaLectura.getTime())) {
        return false;
    }

    const minutosTranscurridos =
        (Date.now() - fechaLectura.getTime()) / 60000;

    return minutosTranscurridos > LIMITE_INACTIVIDAD_MINUTOS;
}

// Detectar fechas futuras o inválidas.
function verificarFechaInconsistente(timestamp) {
    const fechaLectura = new Date(timestamp);

    if (Number.isNaN(fechaLectura.getTime())) {
        return true;
    }

    const diferenciaMinutos =
        (Date.now() - fechaLectura.getTime()) / 60000;

    // Tolerancia de un minuto por diferencias de reloj.
    return diferenciaMinutos < -1;
}

// ==========================================
// ACTIVIDAD 7 - MANEJO DE ERRORES
// ==========================================

function obtenerMensajeError(error) {
    const mensaje = String(error?.message || "");

    if (
        error instanceof TypeError ||
        mensaje.includes("Failed to fetch")
    ) {
        return "No hay conexión con el servidor. " +
            "Comprueba que el backend esté encendido.";
    }

    if (mensaje.includes("404")) {
        return "El recurso solicitado no está disponible.";
    }

    if (
        mensaje.includes("502") ||
        mensaje.includes("503") ||
        mensaje.includes("504")
    ) {
        return "El servidor no está disponible temporalmente. " +
            "Comprueba que el backend esté funcionando.";
    }

    if (mensaje.includes("500")) {
        return "El servidor presentó un error interno.";
    }

    return "No fue posible completar la consulta. " + mensaje;
}

// ==========================================
// ACTIVIDAD 2 - CONSULTAR DISPOSITIVOS
// ==========================================

async function consultarDispositivos() {
    resultado.textContent = "Consultando dispositivos...";
    btnConsultar.disabled = true;

    try {
        const respuesta = await fetch(API_DEVICES_URL, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("Método HTTP: GET");
        console.log("Estado HTTP:", respuesta.status);

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const datos = await respuesta.json();

        console.log("Dispositivos recibidos:", datos);

        resultado.textContent = JSON.stringify(datos, null, 4);

    } catch (error) {
        console.error("Error consultando la API:", error);

        resultado.textContent =
            "No fue posible consultar los dispositivos: " +
            obtenerMensajeError(error);

    } finally {
        btnConsultar.disabled = false;
    }
}

// ==========================================
// ACTIVIDAD 5 - CARGAR DISPOSITIVOS
// ==========================================

async function cargarDispositivos() {
    selectorDispositivo.innerHTML =
        '<option value="">Cargando dispositivos...</option>';

    try {
        const respuesta = await fetch(API_DEVICES_URL, {
            headers: {
                "Accept": "application/json"
            }
        });

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const datos = await respuesta.json();

        const dispositivos = Array.isArray(datos.devices)
            ? datos.devices
            : [];

        selectorDispositivo.innerHTML =
            '<option value="">Seleccione un dispositivo</option>';

        if (dispositivos.length === 0) {
            mostrarMensaje(
                mensajeEstado,
                "advertencia",
                "No hay dispositivos registrados."
            );
            return;
        }

        dispositivos.forEach(dispositivo => {
            const opcion = document.createElement("option");

            opcion.value = dispositivo.device_id;

            opcion.textContent =
                dispositivo.device_id + " - " +
                (dispositivo.name || "Sin nombre");

            selectorDispositivo.appendChild(opcion);
        });

        mostrarMensaje(
            mensajeEstado,
            "informacion",
            "Selecciona un dispositivo y consulta su última lectura."
        );

    } catch (error) {
        console.error("Error cargando dispositivos:", error);

        selectorDispositivo.innerHTML =
            '<option value="">No se pudieron cargar los dispositivos</option>';

        mostrarMensaje(
            mensajeEstado,
            "error",
            "Error al cargar dispositivos: " +
            obtenerMensajeError(error)
        );
    }
}

// ==========================================
// ACTIVIDAD 5 - LIMPIAR TARJETAS
// ==========================================

function limpiarTarjetas() {
    estadoPuerta.textContent = "--";
    tiempoApertura.textContent = "-- segundos";
    accesos.textContent = "--";
    estadoAlerta.textContent = "--";
    fechaActualizacion.textContent = "Sin datos disponibles";
}

// ==========================================
// ACTIVIDAD 5 - CONSULTAR ÚLTIMA LECTURA
// ==========================================

let consultaEstadoEnCurso = false;

async function consultarEstadoActual() {

    if (consultaEstadoEnCurso) {
        return;
    }

    const deviceId = selectorDispositivo.value;

    if (!deviceId) {
        limpiarTarjetas();
        mostrarMensaje(
            mensajeEstado,
            "advertencia",
            "Selecciona un dispositivo."
        );
        return;
    }

    consultaEstadoEnCurso = true;

    if (!deviceId) {
        mostrarMensaje(
            mensajeEstado,
            "advertencia",
            "Selecciona un dispositivo."
        );
        return;
    }

    mostrarMensaje(
        mensajeEstado,
        "informacion",
        "Consultando última lectura..."
    );

    btnEstadoActual.disabled = true;

    try {
        const url =
            `${API_BASE_URL}/api/devices/` +
            `${encodeURIComponent(deviceId)}/latest`;

        const respuesta = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("Endpoint:", url);
        console.log("Estado HTTP:", respuesta.status);

        if (
            respuesta.status === 404 ||
            respuesta.status === 204
        ) {
            mostrarMensaje(
                mensajeEstado,
                "advertencia",
                "Sin lectura disponible para este dispositivo."
            );
            return;
        }

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const datos = await respuesta.json();
        const lectura = datos.latest || datos;

        console.log("Última lectura:", lectura);

        if (!lectura || lectura.timestamp == null) {
            mostrarMensaje(
                mensajeEstado,
                "advertencia",
                "Sin lectura disponible para este dispositivo."
            );
            return;
        }

        // Actualizar tarjetas.
        estadoPuerta.textContent =
            lectura.door_state === "OPEN"
                ? "ABIERTA"
                : lectura.door_state === "CLOSED"
                    ? "CERRADA"
                    : "Desconocido";

        tiempoApertura.textContent =
            lectura.open_duration != null
                ? lectura.open_duration + " segundos"
                : "-- segundos";

        accesos.textContent =
            lectura.access_count ?? "--";

        estadoAlerta.textContent =
            lectura.alert_status ?? "--";

        // Fecha de la última lectura.
        const fecha = new Date(lectura.timestamp);

        fechaActualizacion.textContent =
            Number.isNaN(fecha.getTime())
                ? String(lectura.timestamp)
                : fecha.toLocaleString("es-CO");

        // ======================================
        // ACTIVIDAD 7 - VALIDACIÓN DE ESTADOS
        // ======================================

        // Prioridad 1: alerta reportada por el sensor.
        if (lectura.alert_status === "ALERT") {

            mostrarMensaje(
                mensajeEstado,
                "error",
                "ALERTA DEL DISPOSITIVO: " + deviceId +
                ". Fecha: " + fechaActualizacion.textContent +
                ". Tiempo de apertura: " +
                (lectura.open_duration ?? "No disponible") +
                " segundos. Descripción: El sensor reportó " +
                "una condición que requiere revisión."
            );

        // Prioridad 2: fecha futura o inválida.
        } else if (
            verificarFechaInconsistente(lectura.timestamp)
        ) {

            mostrarMensaje(
                mensajeEstado,
                "error",
                "FECHA INCONSISTENTE: El dispositivo " +
                deviceId +
                " reportó una lectura con fecha futura o inválida. " +
                "Fecha registrada: " +
                fechaActualizacion.textContent +
                ". Verifica la fecha y hora del sensor."
            );

        // Prioridad 3: dispositivo sin lecturas recientes.
        } else if (
            verificarInactividad(lectura.timestamp)
        ) {

            const minutosInactivo = Math.floor(
                (Date.now() - fecha.getTime()) / 60000
            );

            mostrarMensaje(
                mensajeEstado,
                "advertencia",
                "DISPOSITIVO INACTIVO: " + deviceId +
                ". No se han recibido nuevas lecturas durante " +
                minutosInactivo + " minutos. " +
                "Última comunicación: " +
                fechaActualizacion.textContent +
                ". Verifica la conexión del sensor."
            );

        // Prioridad 4: funcionamiento normal.
        } else {

            mostrarMensaje(
                mensajeEstado,
                "exito",
                "Última lectura consultada correctamente. " +
                "El dispositivo " + deviceId +
                " tiene una lectura reciente."
            );
        }

    } catch (error) {
        console.error("Error consultando estado:", error);

        limpiarTarjetas();

        mostrarMensaje(
            mensajeEstado,
            "error",
            obtenerMensajeError(error)
        );

    } finally {
        consultaEstadoEnCurso = false;
    btnEstadoActual.disabled = false;
    }
}

// ==========================================
// ACTIVIDAD 6 - LIMPIAR GRÁFICAS
// ==========================================

function limpiarHistorico() {
    if (typeof Chart !== "undefined") {
        for (const id of [
            "graficaApertura",
            "graficaAccesos"
        ]) {
            const anterior = Chart.getChart(id);

            if (anterior) {
                anterior.destroy();
            }
        }
    }

    graficaApertura = null;
    graficaAccesos = null;

    interpretacionHistorico.textContent =
        "Aquí aparecerá el análisis de las lecturas consultadas.";
}

// ==========================================
// ACTIVIDAD 6 - CONSULTAR HISTÓRICO
// ==========================================

async function consultarHistorico() {
    const deviceId = selectorDispositivo.value;
    const limite = Number(limiteHistorico.value) || 10;

    if (!deviceId) {
        mostrarMensaje(
            mensajeHistorico,
            "advertencia",
            "Selecciona primero un dispositivo."
        );
        return;
    }

    if (typeof Chart === "undefined") {
        mostrarMensaje(
            mensajeHistorico,
            "error",
            "No se pudo cargar la librería de gráficas."
        );
        return;
    }

    btnHistorico.disabled = true;

    mostrarMensaje(
        mensajeHistorico,
        "informacion",
        "Consultando histórico..."
    );

    try {
        const url =
            `${API_BASE_URL}/api/devices/` +
            `${encodeURIComponent(deviceId)}/telemetry`;

        const respuesta = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("Endpoint histórico:", url);
        console.log("Estado HTTP:", respuesta.status);

        if (!respuesta.ok) {
            throw new Error("HTTP " + respuesta.status);
        }

        const datos = await respuesta.json();

        const registros = Array.isArray(datos.telemetry)
            ? datos.telemetry
            : [];

        // Filtrar y ordenar cronológicamente.
        const historico = registros
            .filter(r =>
                r.timestamp &&
                !Number.isNaN(
                    new Date(r.timestamp).getTime()
                ) &&
                r.open_duration != null &&
                r.access_count != null &&
                Number.isFinite(Number(r.open_duration)) &&
                Number.isFinite(Number(r.access_count))
            )
            .sort(
                (a, b) =>
                    new Date(a.timestamp) -
                    new Date(b.timestamp)
            )
            .slice(-limite);

        // Eliminar gráficas anteriores.
        limpiarHistorico();

        if (historico.length === 0) {
            mostrarMensaje(
                mensajeHistorico,
                "advertencia",
                "No hay lecturas históricas disponibles."
            );
            return;
        }

        // Preparar fechas.
        const fechas = historico.map(r =>
            new Date(r.timestamp).toLocaleString(
                "es-CO",
                {
                    day: "2-digit",
                    month: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit"
                }
            )
        );

        // Preparar valores.
        const duraciones = historico.map(
            r => Number(r.open_duration)
        );

        const cantidades = historico.map(
            r => Number(r.access_count)
        );

        // Configuración general.
        const opcionesBase = () => ({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        autoSkip: true
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        });

        // ==================================
        // GRÁFICA 1 - TIEMPO DE APERTURA
        // ==================================

        const opcionesApertura = opcionesBase();

        opcionesApertura.scales.y.title = {
            display: true,
            text: "Segundos"
        };

        graficaApertura = new Chart(
            document.getElementById("graficaApertura"),
            {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Tiempo de apertura (segundos)",
                        data: duraciones,
                        borderColor: "#1976d2",
                        backgroundColor: "rgba(25,118,210,0.12)",
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: opcionesApertura
            }
        );

        // ==================================
        // GRÁFICA 2 - ACCESOS REGISTRADOS
        // ==================================

        const opcionesAccesos = opcionesBase();

        opcionesAccesos.scales.y.ticks = {
            precision: 0
        };

        opcionesAccesos.scales.y.title = {
            display: true,
            text: "Accesos"
        };

        graficaAccesos = new Chart(
            document.getElementById("graficaAccesos"),
            {
                type: "line",
                data: {
                    labels: fechas,
                    datasets: [{
                        label: "Accesos registrados",
                        data: cantidades,
                        borderColor: "#198754",
                        backgroundColor: "rgba(25,135,84,0.12)",
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: opcionesAccesos
            }
        );

        // ==================================
        // INTERPRETACIÓN DEL HISTÓRICO
        // ==================================

        const maxApertura = Math.max(...duraciones);

        const alertas = historico.filter(
            r => r.alert_status === "ALERT"
        ).length;

        mostrarMensaje(
            mensajeHistorico,
            "informacion",
            `Histórico cargado: ${historico.length} lecturas.`
        );

        interpretacionHistorico.textContent =
            `El dispositivo ${deviceId} registró una ` +
            `apertura máxima de ${maxApertura} segundos. ` +
            `Se identificaron ${alertas} lecturas en estado ALERT. ` +
            `Estas gráficas permiten observar cambios en los tiempos ` +
            `de apertura y en el contador de accesos, facilitando ` +
            `la identificación de comportamientos que requieren revisión.`;

    } catch (error) {
        console.error(
            "Error consultando histórico:",
            error
        );

        limpiarHistorico();

        mostrarMensaje(
            mensajeHistorico,
            "error",
            "No fue posible consultar el histórico: " +
            obtenerMensajeError(error)
        );

    } finally {
        btnHistorico.disabled = false;
    }
}

// ==========================================
// EVENTOS - REGISTRADOS UNA SOLA VEZ
// ==========================================

btnConsultar.addEventListener(
    "click",
    consultarDispositivos
);

btnEstadoActual.addEventListener(
    "click",
    consultarEstadoActual
);

btnHistorico.addEventListener(
    "click",
    consultarHistorico
);

selectorDispositivo.addEventListener(
    "change",
    () => {
        limpiarTarjetas();
        limpiarHistorico();

        mostrarMensaje(
            mensajeEstado,
            "informacion",
            "Presiona Consultar última lectura."
        );

        mostrarMensaje(
            mensajeHistorico,
            "informacion",
            "Presiona Consultar histórico para cargar las gráficas."
        );
    }
);

// ==========================================
// INICIALIZACIÓN DEL SISTEMA
// ==========================================

cargarDispositivos();

// ==========================================
// ACTIVIDAD 8 - ACTUALIZACIÓN CONTROLADA
// ==========================================

const INTERVALO_ACTUALIZACION = 15000;

setInterval(() => {

    if (
        document.visibilityState === "visible" &&
        selectorDispositivo.value &&
        !consultaEstadoEnCurso
    ) {
        consultarEstadoActual();
    }

}, INTERVALO_ACTUALIZACION);
