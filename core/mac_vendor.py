"""
Servicio para detectar el fabricante (vendor) de dispositivos de red
basándose en su dirección MAC (OUI - Organizationally Unique Identifier).
"""

import requests
from typing import Dict


class MacVendorService:
    """
    Servicio que consulta la API de macvendors.com para obtener
    información del fabricante de una dirección MAC.
    
    Implementa caché local para evitar consultas repetidas y mejorar
    el rendimiento en escaneos subsecuentes.
    """
    
    def __init__(self):
        """Inicializa el servicio con un caché vacío."""
        self.cache: Dict[str, str] = {}
        self.api_url = "https://api.macvendors.com/"
        self.timeout = 2  # Timeout de 2 segundos para consultas HTTP
    
    def get_vendor(self, mac_address: str) -> str:
        """
        Obtiene el nombre del fabricante para una dirección MAC.
        
        Args:
            mac_address: Dirección MAC en formato estándar (ej: "AA:BB:CC:DD:EE:FF")
        
        Returns:
            Nombre del fabricante o "Unknown" si no se puede determinar.
        
        Examples:
            >>> service = MacVendorService()
            >>> service.get_vendor("00:1A:2B:3C:4D:5E")
            'Apple, Inc.'
        """
        # Validar formato básico de MAC
        if not mac_address or len(mac_address) < 8:
            return "Unknown"
        
        # Normalizar MAC address (convertir a mayúsculas para consistencia)
        mac_normalized = mac_address.upper()
        
        # Verificar si ya está en caché
        if mac_normalized in self.cache:
            return self.cache[mac_normalized]
        
        # Consultar API
        try:
            response = requests.get(
                f"{self.api_url}{mac_address}",
                timeout=self.timeout
            )
            
            # Si la respuesta es exitosa (200)
            if response.status_code == 200:
                vendor = response.text.strip()
                self.cache[mac_normalized] = vendor
                return vendor
            
            # Si no se encuentra (404) o cualquier otro error
            else:
                self.cache[mac_normalized] = "Unknown"
                return "Unknown"
                
        except requests.exceptions.Timeout:
            # Timeout: no bloquear la aplicación
            print(f"Timeout consultando vendor para {mac_address}")
            return "Unknown"
            
        except requests.exceptions.RequestException as e:
            # Error de red: manejar de forma elegante
            print(f"Error consultando vendor para {mac_address}: {e}")
            return "Unknown"
            
        except Exception as e:
            # Cualquier otro error inesperado
            print(f"Error inesperado consultando vendor: {e}")
            return "Unknown"
