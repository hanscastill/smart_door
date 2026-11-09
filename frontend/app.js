
 // ==========================================
 // SMARTDOOR - CONEXIÓN FRONTEND CON API
 // ACTIVIDAD 2
 // ==========================================

 const btnConsultar = document.getElementById("btnConsultar");
 const resultado = document.getElementById("resultado");

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
             throw new Error(
                 "Error HTTP: " + respuesta.status
             );
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

 btnConsultar.addEventListener(
     "click",
     consultarDispositivos
 );
