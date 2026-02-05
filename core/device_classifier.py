"""
Clasificador de dispositivos basado en Vendor, MAC o IP.
Ayuda a asignar iconos apropiados en la visualización de topología.
"""

from enum import Enum


class DeviceType(Enum):
    ROUTER = "router"
    PC = "pc"
    PHONE = "phone"
    TABLET = "tablet"
    PRINTER = "printer"
    TV = "tv"
    GAME_CONSOLE = "game_console"
    UNKNOWN = "unknown"


class DeviceClassifier:
    """Clasifica dispositivos en tipos conocidos."""
    
    # Palabras clave en vendors para clasificación
    KEYWORDS = {
        DeviceType.PHONE: ["Apple", "Samsung", "Xiaomi", "Huawei", "OnePlus", "Motorola", "Pixel"],
        DeviceType.PC: ["Dell", "Lenovo", "HP", "Hewlett Packard", "ASUS", "Acer", "MSI", "Intel", "Giga-Byte"],
        DeviceType.ROUTER: ["Cisco", "TP-Link", "Netgear", "Ubiquiti", "D-Link", "Linksys", "Huawei Technologies"],
        DeviceType.PRINTER: ["Canon", "Epson", "Brother", "Xerox"],
        DeviceType.TV: ["LG", "Sony", "Roku", "TCL"],
        DeviceType.GAME_CONSOLE: ["Nintendo", "Sony Interactive", "Microsoft"],
    }
    
    @classmethod
    def classify(cls, mac: str, vendor: str, ip: str) -> DeviceType:
        """
        Clasifica un dispositivo basado en sus atributos.
        
        Args:
            mac: Dirección MAC
            vendor: Fabricante detectado
            ip: Dirección IP
            
        Returns:
            Tipo de dispositivo (DeviceType)
        """
        if not vendor:
            vendor = ""
            
        # 1. Regla especial: Gateway suele ser el .1
        if ip.endswith(".1"):
            return DeviceType.ROUTER
        
        # 2. Búsqueda por palabras clave en Vendor
        vendor_lower = vendor.lower()
        
        for dtype, keywords in cls.KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in vendor_lower:
                    # Refinamiento para Apple (puede ser Mac o iPhone)
                    if "apple" in vendor_lower:
                        # Asumimos Phone por defecto para Apple en redes domésticas
                        # salvo que tengamos algo más específico (difícil sin Nmap)
                        pass 
                    return dtype
        
        # 3. Fallback
        return DeviceType.UNKNOWN
