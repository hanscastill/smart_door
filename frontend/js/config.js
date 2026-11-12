
 // ==========================================
 // SMARTDOOR - CONFIGURACIÓN DE LA API
 // ACTIVIDADES 2 Y 3
 // ==========================================

 // Backend FastAPI en el mismo origen
 const API_BASE_URL = window.location.origin;

 // Endpoint para consultar dispositivos
 const API_DEVICES_URL = `${API_BASE_URL}/api/devices`;

 console.log("API SmartDoor configurada:", API_BASE_URL);
