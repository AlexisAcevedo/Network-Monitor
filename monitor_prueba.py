import psutil
import time

def convertir_bytes(tamanio):
    """Función auxiliar para convertir bytes a KB o MB para que sea legible."""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanio < 1024:
            return f"{tamanio:.2f} {unidad}"
        tamanio /= 1024

print("--- Iniciando Monitor de Red (Ctrl + C para salir) ---")

# 1. TOMA DE DATOS INICIAL (T0)
# Obtenemos el total de bytes transmitidos desde que se prendió la PC hasta AHORA.
io_inicial = psutil.net_io_counters()
bytes_enviados_anteriores = io_inicial.bytes_sent
bytes_recibidos_anteriores = io_inicial.bytes_recv

while True:
    # 2. EL INTERVALO
    # Esperamos 1 segundo exacto para medir la velocidad en "bytes por segundo".
    time.sleep(1)

    # 3. TOMA DE DATOS ACTUAL (T1)
    io_actual = psutil.net_io_counters()
    
    # Extraemos los nuevos totales acumulados
    bytes_enviados_nuevos = io_actual.bytes_sent
    bytes_recibidos_nuevos = io_actual.bytes_recv

    # 4. EL CÁLCULO DIFERENCIAL (Delta)
    # Restamos el total actual menos el total anterior para saber cuánto pasó en este segundo.
    velocidad_subida = bytes_enviados_nuevos - bytes_enviados_anteriores
    velocidad_bajada = bytes_recibidos_nuevos - bytes_recibidos_anteriores

    # 5. MOSTRAR RESULTADOS
    # Usamos la función auxiliar para que no nos muestre "1048576 bytes" sino "1.00 MB"
    print(f"Subida: {convertir_bytes(velocidad_subida)}/s  |  Bajada: {convertir_bytes(velocidad_bajada)}/s")

    # 6. ACTUALIZAR REFERENCIA
    # Los datos "nuevos" de hoy, pasan a ser los "anteriores" para la siguiente vuelta del bucle.
    bytes_enviados_anteriores = bytes_enviados_nuevos
    bytes_recibidos_anteriores = bytes_recibidos_nuevos