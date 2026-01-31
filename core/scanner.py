from asyncio import timeout
from _socket import socket
import scapy.all as scapy
import socket
from core.mac_vendor import MacVendorService

class NetworkScanner:
    def __init__(self):
        # Intentamos detectar nuestra IP local y el rango (ej: 192.168.1.1/24)
        self.target_ip = self.get_local_range()
        # Servicio para detectar fabricantes de dispositivos
        self.vendor_service = MacVendorService()
        # Set de MACs conocidas para detectar nuevos dispositivos
        self.known_devices = set()

    def get_local_range(self):
        """Detecta la IP de nuestra PC y calcula el rango de la red local"""
        try:
            # Obtenemos IP local sin conectar realmente a internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Calculamos el rango (ej: 192.168.1.1 -> 192.168.1.1/24)
            ip_parts = local_ip.split(".")
            network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1/24"
            return network_range
        except Exception as e:
            print(f"Error detecting local IP: {e}")
            return "192.168.1.1/24"  # Fallback por defecto
    
    def scan_network(self):
        """
        Escanea la red local usando ARP y retorna lista de dispositivos
        """
        try:
            print(f"Scanning target: {self.target_ip}...")
            
            # 1. Crear paquete ARP
            arp_request = scapy.ARP(pdst=self.target_ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # 2. Enviar y recibir respuestas
            # Espera solo 1 segundo (timeout) para no congelar la pantalla
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            
            # 3. Procesar resultados
            clients_list = []
            for element in answered_list:
                # element[1] es el paquete de respuesta (p.answer)
                ip_address = element[1].psrc
                mac_address = element[1].hwsrc
                client_dict = {
                    "ip": ip_address,
                    "mac": mac_address,
                    "vendor": self.vendor_service.get_vendor(mac_address)
                }
                clients_list.append(client_dict)
                
            return clients_list
            
        except Exception as e:
            print(f"Error scanning: {e}")
            return []
    
    def detect_new_devices(self, current_scan: list) -> list:
        """
        Detecta dispositivos nuevos comparando con dispositivos conocidos.
        
        Args:
            current_scan: Lista de dispositivos del escaneo actual
            
        Returns:
            Lista de dispositivos nuevos (no vistos antes)
        """
        new_devices = []
        
        for device in current_scan:
            mac = device.get('mac')
            if mac and mac not in self.known_devices:
                new_devices.append(device)
                self.known_devices.add(mac)
        
        return new_devices