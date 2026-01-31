import asyncio
import flet as ft
import asyncio
from ui.device_list import create_device_table

class ScannerView(ft.Column):
    def __init__(self, scanner_service, page: ft.Page, notification_service=None):
        super().__init__()
        self.scanner = scanner_service # El servicio de escaneo
        self.main_page = page
        self.notification_service = notification_service  # Servicio de notificaciones
        self.visible = False # Esta vista arranca oculta
        
        # Almacenamiento de dispositivos
        self.all_devices = []  # Lista completa de dispositivos
        self.filter_text = ""  # Texto del filtro actual
        self.device_alerts_enabled = True  # Alertas de nuevos dispositivos habilitadas por defecto

        # 1. Crear la tabla
        self.table = create_device_table()

        # 2. Crear el boton de escaneo
        self.btn = ft.Button(
            "Scan Network",
            icon=ft.Icons.RADAR,
            on_click=self.run_scan,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white"
        )
        
        # 3. Crear campo de búsqueda
        self.search_field = ft.TextField(
            hint_text="Search by IP, MAC or Vendor...",
            on_change=self.apply_filter,
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            height=50
        )
        
        # 4. Crear botón de limpiar filtro
        self.clear_btn = ft.IconButton(
            icon=ft.Icons.CLEAR,
            on_click=self.clear_filter,
            tooltip="Limpiar filtro"
        )

        # 5. Armar el Layout (lo que se ve en pantalla)
        self.controls = [
            ft.Text("Network Device Scanner", size=20, weight="bold"),
            
            # Fila 1: Descripción y botón de escaneo
            ft.Row(
                [ft.Text("Detect connected devices via ARP Protocol"), self.btn], 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            
            # Fila 2: Búsqueda y filtros
            ft.Row(
                [self.search_field, self.clear_btn]
            ),
            
            ft.Divider(), # Línea separadora
            self.table    # La tabla
        ]
    
    async def run_scan(self, e):
        """Logica interna: Ejecuta el escaneo y actualiza la tabla"""
        # A) Estado "Cargando"
        self.btn.disabled=True
        self.btn.text = "Scanning..."
        self.btn.icon = ft.Icons.HOURGLASS_TOP
        self.main_page.update()

        try:
            # B) Ejecutar escaneo en segundo plano para no congelar la app
            devices = await asyncio.to_thread(self.scanner.scan_network)
            
            # Detectar nuevos dispositivos y notificar
            if self.notification_service and self.device_alerts_enabled:
                new_devices = self.scanner.detect_new_devices(devices)
                for device in new_devices:
                    self.notification_service.notify_new_device(device)
            
            # Guardar todos los dispositivos
            self.all_devices = devices

            # C) Llenar la tabla con resultados
            self._update_table(devices)
        except Exception as e:
            print(f"Error scanning: {e}")

        # D) Restaurar boton
        self.btn.disabled=False
        self.btn.text = "Scan network"
        self.btn.icon = ft.Icons.RADAR
        self.main_page.update()
    
    def apply_filter(self, e):
        """Filtra dispositivos según el texto ingresado."""
        if not self.all_devices:
            return
        
        filter_text = self.search_field.value.lower().strip()
        
        if not filter_text:
            # Si el filtro está vacío, mostrar todos
            self._update_table(self.all_devices)
            return
        
        # Filtrar dispositivos
        filtered = []
        for dev in self.all_devices:
            # Buscar en IP, MAC y Vendor
            if (filter_text in dev.get('ip', '').lower() or
                filter_text in dev.get('mac', '').lower() or
                filter_text in dev.get('vendor', 'Unknown').lower()):
                filtered.append(dev)
        
        self._update_table(filtered)
    
    def clear_filter(self, e):
        """Limpia el filtro y muestra todos los dispositivos."""
        self.search_field.value = ""
        self._update_table(self.all_devices)
        self.main_page.update()
    
    def _update_table(self, devices):
        """Actualiza la tabla con la lista de dispositivos proporcionada."""
        self.table.rows.clear()
        for dev in devices:
            self.table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(dev['ip'])),
                    ft.DataCell(ft.Text(dev['mac'], font_family="Consolas")),
                    ft.DataCell(ft.Text(dev.get('vendor', 'Unknown'), size=12)),
                    ft.DataCell(ft.Icon(ft.Icons.CIRCLE, color="green", size=10)),
                ])
            )
        self.main_page.update()
    
    def toggle_alerts(self, e):
        """Activa/desactiva las alertas de nuevos dispositivos."""
        self.device_alerts_enabled = self.alerts_toggle.value
