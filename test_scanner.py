from core.scanner import NetworkScanner
import time

print("--- INICIANDO DIAGNÓSTICO DE RED ---")
scanner = NetworkScanner()
print(f"Rango de red detectado: {scanner.target_ip}")
print("Escaneando... (Espera unos segundos)")

start = time.time()
devices = scanner.scan_network()
end = time.time()

print(f"\nEscaneo completado en {end - start:.2f} segundos.")
print(f"Dispositivos encontrados: {len(devices)}")
print("-" * 40)
print(f"{'IP ADDRESS':<20} {'MAC ADDRESS'}")
print("-" * 40)

for device in devices:
    print(f"{device['ip']:<20} {device['mac']}")