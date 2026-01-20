from asyncio import timeout
from _socket import socket
import scapy.all as scapy
import socket

class NetworkScanner:
    def __init__(self):
        # Intentamos detectar nuestra IP local y el rango (ej: 192.168.1.1/24)
        self.target_ip = self.get_local_range()

    def get_local_range(self):
        """Detecta la IP de nuestra PC y calcula el rango de la red local"""
        try:
            # Obtenemos IP local sin conectar realmente a internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # Cortamos el ultimo numero y agregamos .1/24 para escanera toda la subred
            # Ejemplo: Si tu IP es 192.168.0.45 -> Rango: 192.168.0.1/24
            base_ip = ".".join(local_ip.split(".")[:-1]) + ".1/24"
            return base_ip
        except:
            # Fallback por si falla la deteccion automatica
            return "192.168.1.1/24"

    def scan_network(self):
        """
        Envía peticiones ARP a toda la red.
        """
        print(f"Scanning target: {self.target_ip}...") # Debug
        
        try:
            # DEFINICIÓN DE PAQUETES
            
            # 1. ARP Request: ¿Quién tiene esta IP?
            arp_request = scapy.ARP(pdst=self.target_ip)
            
            # 2. Ethernet Frame: Broadcast a todos (FF:FF:FF...)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            
            # 3. FUSIÓN
            arp_request_broadcast = broadcast / arp_request
            
            # 4. Enviar y esperar respuesta
            # Espera solo 1 segundo (timeout) para no congelar la pantalla
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
            
            clients_list = []
            for element in answered_list:
                # element[1] es el paquete de respuesta (p.answer)
                client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
                clients_list.append(client_dict)
                
            return clients_list
            
        except Exception as e:
            print(f"Error scanning: {e}")
            return []