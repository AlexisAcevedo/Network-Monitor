"""
Vista de Topología de Red.
Muestra una visualización jerárquica (árbol) de los dispositivos.
"""

import flet as ft
from core.device_classifier import DeviceClassifier, DeviceType
from core.scanner import NetworkScanner


def TopologyView(scanner_service: NetworkScanner, page: ft.Page):
    """
    Crea la vista de Topología.
    Muestra un árbol visual con el Router arriba y dispositivos conectados.
    """
    
    # Estado local
    devices = []
    
    # Mapeo de Tipos a Iconos Flet
    ICON_MAP = {
        DeviceType.ROUTER: ft.Icons.ROUTER,
        DeviceType.PC: ft.Icons.COMPUTER,
        DeviceType.PHONE: ft.Icons.PHONE_ANDROID,
        DeviceType.TABLET: ft.Icons.TABLET,
        DeviceType.PRINTER: ft.Icons.PRINT,
        DeviceType.TV: ft.Icons.TV,
        DeviceType.GAME_CONSOLE: ft.Icons.GAMEPAD,
        DeviceType.UNKNOWN: ft.Icons.DEVICE_UNKNOWN,
    }
    
    # Contenedor principal de la topología
    topology_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=40
    )
    
    status_text = ft.Text("Waiting...", color=ft.Colors.WHITE54)
    refresh_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        tooltip="Refresh Topology",
        on_click=lambda e: load_topology()
    )
    
    def get_device_card(device):
        """Crea una tarjeta visual para un nodo dispositivo."""
        ip = device.get("ip", "Unknown")
        mac = device.get("mac", "Unknown")
        vendor = device.get("vendor", "Unknown")
        
        # Clasificar
        dtype = DeviceClassifier.classify(mac, vendor, ip)
        icon = ICON_MAP.get(dtype, ft.Icons.DEVICE_UNKNOWN)
        
        # Color del ícono según tipo
        icon_color = ft.Colors.CYAN if dtype == DeviceType.ROUTER else ft.Colors.WHITE70
        
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=icon_color),
                ft.Text(ip, weight="bold", size=12),
                ft.Text(vendor[:15] + "..." if len(vendor) > 15 else vendor, size=10, color=ft.Colors.WHITE54),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=10,
            bgcolor=ft.Colors.BLACK_26,
            border_radius=8,
            width=100,
            height=100,
            tooltip=f"IP: {ip}\nMAC: {mac}\nVendor: {vendor}\nType: {dtype.value}"
        )
    
    def load_topology():
        """Carga y dibuja la topología."""
        status_text.value = "Updating topology..."
        status_text.color = ft.Colors.AMBER
        topology_container.controls.clear()
        page.update()
        
        # Obtener dispositivos (reusamos lógica del scanner)
        # Nota: Idealmente deberíamos cachear esto o pasarlo desde el main
        try:
            current_devices = scanner_service.scan_network()
            
            # Buscar el Gateway/Router (normalmente termina en .1)
            router = next((d for d in current_devices if d.get("ip", "").endswith(".1")), None)
            
            # Si no encontramos router explícito, creamos uno virtual
            if not router:
                router = {"ip": "Gateway", "mac": "", "vendor": "Router"}
            
            # El resto son clientes
            clients = [d for d in current_devices if d != router]
            
            # --- CONSTRUCCIÓN VISUAL ---
            
            # 1. Nivel Superior: Router
            router_node = get_device_card(router)
            
            # 2. Conector Central (Línea vertical)
            connector_line = ft.Container(
                width=2, height=40, bgcolor=ft.Colors.GREY_700
            )
            
            # 3. Nivel Inferior: Clientes (Grid)
            # Usamos Wrap para que se acomoden responsive
            clients_wrap = ft.Row(
                wrap=True,
                spacing=20,
                run_spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[get_device_card(c) for c in clients]
            )
            
            # Armar árbol
            topology_container.controls = [
                router_node,
                connector_line,
                clients_wrap
            ]
            
            status_text.value = f"Topology mapped. {len(clients) + 1} devices found."
            status_text.color = ft.Colors.GREEN
            
        except Exception as e:
            status_text.value = f"Error loading topology: {e}"
            status_text.color = ft.Colors.RED
        
        page.update()

    # Layout Principal
    view = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Network Topology", size=24, weight="bold"),
                    ft.Container(expand=True),
                    status_text,
                    refresh_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(color=ft.Colors.GREY_800),
            ft.Container(
                content=topology_container,
                expand=True,
                padding=20,
                # border=ft.border.all(1, ft.Colors.GREY_800),
                # border_radius=10
            )
        ],
        expand=True,
        visible=False
    )
    
    return view, load_topology
