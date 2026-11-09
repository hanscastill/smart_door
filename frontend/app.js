
 // ==========================================
 // SMARTDOOR - FRONTEND
 // ACTIVIDADES 2 Y 5
 // ==========================================

 const btnConsultar = document.getElementById("btnConsultar");
 const resultado = document.getElementById("resultado");

 const selectorDispositivo =
     document.getElementById("selectorDispositivo");

 const btnEstadoActual =
     document.getElementById("btnEstadoActual");

 const estadoPuerta =
     document.getElementById("estadoPuerta");

 const tiempoApertura =
     document.getElementById("tiempoApertura");

 const accesos =
     document.getElementById("accesos");

 const estadoAlerta =
     document.getElementById("estadoAlerta");

 const fechaActualizacion =
     document.getElementById("fechaActualizacion");

 const mensajeEstado =
     document.getElementById("mensajeEstado");


 // ==========================================
 // ACTIVIDAD 2 - CONSULTAR DISPOSITIVOS
 // ==========================================

 async function consultarDispositivos() {

     resultado.textContent = "Consultando dispositivos...";

     try {

         const respuesta = await fetch(API_DEVICES_URL, {
             method: "GET",
             headers: {
                 "Accept": "application/json"
             }
         });

         console.log("Método HTTP:", "GET");
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
     }
 }


 // ==========================================
 // ACTIVIDAD 5 - CARGAR SELECTOR
 // ==========================================

 async function cargarDispositivos() {

     selectorDispositivo.innerHTML =
         '<option value="">Cargando dispositivos...</option>';

     try {

         const respuesta = await fetch(API_DEVICES_URL);

         if (!respuesta.ok) {
             throw new Error("HTTP " + respuesta.status);
         }

         const datos = await respuesta.json();

         selectorDispositivo.innerHTML =
             '<option value="">Seleccione un dispositivo</option>';

         const dispositivos = datos.devices || [];

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
                 dispositivo.name;

             selectorDispositivo.appendChild(opcion);
         });

         mensajeEstado.textContent =
             "Selecciona un dispositivo y consulta su última lectura.";

     } catch (error) {

         console.error("Error cargando dispositivos:", error);

         selectorDispositivo.innerHTML =
             '<option value="">No se pudieron cargar los dispositivos</option>';

         mensajeEstado.textContent =
             "Error al cargar dispositivos: " + error.message;
     }
 }


 // ==========================================
 // LIMPIAR TARJETAS
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

         // Manejar ausencia de lecturas
         if (respuesta.status === 404 ||
             respuesta.status === 204) {

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

         console.log("Última lectura:", datos);

         // Aceptar respuesta directa o anidada
         const lectura = datos.latest || datos;

         if (!lectura ||
             lectura.timestamp == null) {

             mensajeEstado.textContent =
                 "Sin lectura disponible para este dispositivo.";

             return;
         }

         // Mostrar variables principales
         estadoPuerta.textContent =
             lectura.door_state === "OPEN" ? "ABIERTA" :
             lectura.door_state === "CLOSED" ? "CERRADA" :
             "Desconocido";

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
 // EVENTOS
 // ==========================================

 btnConsultar.addEventListener(
     "click",
     consultarDispositivos
 );

 btnEstadoActual.addEventListener(
     "click",
     consultarEstadoActual
 );

 selectorDispositivo.addEventListener(
     "change",
     () => {
         limpiarTarjetas();
         mensajeEstado.textContent =
             "Presiona Consultar última lectura.";
     }
 );

 // Cargar dispositivos al abrir la página
 cargarDispositivos();
