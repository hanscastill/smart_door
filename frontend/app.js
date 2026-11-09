
// ==========================================
// SMARTDOOR - FRONTEND
// ACTIVIDADES 2, 5 Y 6
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
            throw new Error("Error HTTP: " + respuesta.status);
        }

        const datos = await respuesta.json();

        console.log("Dispositivos recibidos:", datos);

        resultado.textContent = JSON.stringify(
            datos,
            null,
            4
        );

    } catch (error) {

        console.error("Error consultando la API:", error);

        resultado.textContent =
            "No fue posible consultar los dispositivos: " +
            error.message;

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

            mensajeEstado.textContent =
                "No hay dispositivos registrados.";

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

        mensajeEstado.textContent =
            "Selecciona un dispositivo y consulta su última lectura.";

    } catch (error) {

        console.error("Error cargando dispositivos:", error);

        selectorDispositivo.innerHTML =
            '<option value="">No se pudieron cargar los dispositivos</option>';

        mensajeEstado.textContent =
            "Error al cargar dispositivos: " +
            error.message;
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

    fechaActualizacion.textContent =
        "Sin datos disponibles";
}

// ==========================================
// ACTIVIDAD 5 - CONSULTAR ÚLTIMA LECTURA
// ==========================================

async function consultarEstadoActual() {

    const deviceId = selectorDispositivo.value;

    limpiarTarjetas();

    if (!deviceId) {

        mensajeEstado.textContent =
            "Selecciona un dispositivo.";

        return;
    }

    mensajeEstado.textContent =
        "Consultando última lectura...";

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

            mensajeEstado.textContent =
                "Sin lectura disponible para este dispositivo.";

            return;
        }

        if (!respuesta.ok) {

            throw new Error(
                "Error HTTP: " + respuesta.status
            );
        }

        const datos = await respuesta.json();

        const lectura = datos.latest || datos;

        console.log("Última lectura:", lectura);

        if (!lectura || lectura.timestamp == null) {

            mensajeEstado.textContent =
                "Sin lectura disponible para este dispositivo.";

            return;
        }

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

        const fecha = new Date(lectura.timestamp);

        fechaActualizacion.textContent =
            Number.isNaN(fecha.getTime())
                ? lectura.timestamp
                : fecha.toLocaleString("es-CO");

        mensajeEstado.textContent =
            "Última lectura consultada correctamente.";

    } catch (error) {

        console.error("Error consultando estado:", error);

        limpiarTarjetas();

        mensajeEstado.textContent =
            "No fue posible consultar la última lectura: " +
            error.message;

    } finally {

        btnEstadoActual.disabled = false;
    }
}

// ==========================================
// ACTIVIDAD 6 - LIMPIAR GRÁFICAS
// ==========================================

function limpiarHistorico() {

    if (typeof Chart !== "undefined") {

        // Destruir las instancias existentes.
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

    const limite =
        Number(limiteHistorico.value) || 10;

    if (!deviceId) {

        mensajeHistorico.textContent =
            "Selecciona primero un dispositivo.";

        return;
    }

    if (typeof Chart === "undefined") {

        mensajeHistorico.textContent =
            "No se pudo cargar la librería de gráficas.";

        return;
    }

    btnHistorico.disabled = true;

    mensajeHistorico.textContent =
        "Consultando histórico...";

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
                Number.isFinite(
                    Number(r.open_duration)
                ) &&
                Number.isFinite(
                    Number(r.access_count)
                )
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

            mensajeHistorico.textContent =
                "No hay lecturas históricas disponibles.";

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

        // Configuración general de las gráficas.
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
                        backgroundColor:
                            "rgba(25,118,210,0.12)",
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
                        backgroundColor:
                            "rgba(25,135,84,0.12)",
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

        mensajeHistorico.textContent =
            `Histórico cargado: ${historico.length} lecturas.`;

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

        mensajeHistorico.textContent =
            "No fue posible consultar el histórico: " +
            error.message;

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

        mensajeEstado.textContent =
            "Presiona Consultar última lectura.";

        mensajeHistorico.textContent =
            "Presiona Consultar histórico para cargar las gráficas.";
    }
);

// ==========================================
// INICIALIZACIÓN DEL SISTEMA
// ==========================================

// Cargar dispositivos al abrir la página.
cargarDispositivos();
