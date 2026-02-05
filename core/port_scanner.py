"""
Escáner de puertos multi-hilo usando socket.
Permite escanear puertos específicos o rangos en una IP dada.
"""

import socket
import concurrent.futures
from enum import Enum


class ScanMode(Enum):
    QUICK = "quick"      # Top 20 puertos
    STANDARD = "standard" # Top 100 puertos
    FULL = "full"        # Rango 1-1024


class PortScanner:
    """Escáner de puertos TCP."""
    
    # Puertos comunes para Quick Scan
    TOP_20_PORTS = [
        20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 
        143, 443, 445, 993, 995, 3306, 3389, 5432, 8080, 8443
    ]
    
    # Puertos para Standard Scan (Top 20 + otros comunes)
    TOP_100_PORTS = TOP_20_PORTS + [
        # Web & DB
        8000, 8008, 8888, 27017, 6379, 1433,
        # Mail & File
        111, 161, 465, 587, 2049,
        # Remote Access
        5900, 5901, 5631,
        # IoT / Smart Home
        1883, 5353, 5683, 
        # Games
        25565, 27015
    ] # (Simplificado para el ejemplo, podríamos llenar más)

    @staticmethod
    def get_service_name(port: int) -> str:
        """Obtiene el nombre del servicio para un puerto (si existe)."""
        try:
            return socket.getservbyport(port, "tcp")
        except:
            return "unknown"

    def scan_port(self, ip: str, port: int, timeout: float = 0.5) -> dict | None:
        """
        Intenta conectar a un puerto específico.
        Retorna dict con info si está abierto, None si está cerrado.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    return {
                        "port": port,
                        "state": "open",
                        "service": self.get_service_name(port)
                    }
        except:
            pass
        return None

    def scan(self, ip: str, mode: ScanMode = ScanMode.QUICK) -> list:
        """
        Escanea puertos en la IP dada según el modo seleccionado.
        Usa ThreadPoolExecutor para velocidad.
        """
        ports_to_scan = []
        timeout = 0.5
        
        if mode == ScanMode.QUICK:
            ports_to_scan = self.TOP_20_PORTS
            timeout = 0.5
        elif mode == ScanMode.STANDARD:
            ports_to_scan = self.TOP_100_PORTS
            timeout = 0.3
        elif mode == ScanMode.FULL:
            ports_to_scan = range(1, 1025)
            timeout = 0.1
            
        open_ports = []
        
        # Ejecutar escaneos en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_port = {
                executor.submit(self.scan_port, ip, port, timeout): port 
                for port in ports_to_scan
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result:
                    open_ports.append(result)
                    
        return sorted(open_ports, key=lambda x: x["port"])
