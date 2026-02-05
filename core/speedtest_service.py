"""
Servicio de Speedtest para medir velocidad de internet.
Usa speedtest-cli para conectar con servidores de Ookla.
"""

import speedtest


class SpeedtestService:
    """
    Servicio para ejecutar tests de velocidad de internet.
    Mide download, upload y latencia (ping).
    """
    
    def __init__(self):
        """Inicializa el servicio de speedtest."""
        self._speedtest = None
        self._last_result = None
    
    def _get_client(self) -> speedtest.Speedtest:
        """Obtiene o crea instancia de speedtest."""
        if self._speedtest is None:
            self._speedtest = speedtest.Speedtest()
        return self._speedtest
    
    def run_test(self) -> dict:
        """
        Ejecuta un test completo de velocidad.
        
        Returns:
            dict con download_mbps, upload_mbps, ping_ms, server_name
            En caso de error, retorna dict con error=True
        """
        try:
            client = self._get_client()
            
            # Seleccionar mejor servidor
            client.get_best_server()
            server_info = client.results.server
            
            # Ejecutar tests
            download_bps = client.download()
            upload_bps = client.upload()
            
            # Convertir a Mbps
            download_mbps = download_bps / 1_000_000
            upload_mbps = upload_bps / 1_000_000
            
            # Obtener ping del resultado
            ping_ms = client.results.ping
            
            # Nombre del servidor
            server_name = f"{server_info['sponsor']} ({server_info['name']})"
            
            self._last_result = {
                "download_mbps": round(download_mbps, 2),
                "upload_mbps": round(upload_mbps, 2),
                "ping_ms": round(ping_ms, 1),
                "server_name": server_name,
                "error": False
            }
            
            return self._last_result
            
        except Exception as e:
            return {
                "download_mbps": 0,
                "upload_mbps": 0,
                "ping_ms": 0,
                "server_name": "Error",
                "error": True,
                "error_message": str(e)
            }
    
    def get_servers(self) -> list:
        """
        Obtiene lista de servidores disponibles.
        
        Returns:
            Lista de dicts con información de servidores
        """
        try:
            client = self._get_client()
            client.get_servers()
            
            servers = []
            for server_list in client.servers.values():
                for server in server_list:
                    servers.append({
                        "id": server["id"],
                        "name": server["name"],
                        "sponsor": server["sponsor"],
                        "country": server["country"],
                        "latency": server.get("latency", 0)
                    })
            
            # Ordenar por latencia
            servers.sort(key=lambda x: x["latency"] if x["latency"] else 9999)
            
            return servers[:10]  # Top 10 servers
            
        except Exception:
            return []
    
    def get_last_result(self) -> dict | None:
        """Retorna el último resultado de test."""
        return self._last_result
