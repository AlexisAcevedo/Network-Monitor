import asyncio
import flet as ft
from ui.device_list import create_device_table
from core.port_scanner import PortScanner, ScanMode

class ScannerView(ft.Column):
    def __init__(self, scanner_service, page: ft.Page, notification_service=None):
        super().__init__()
        self.scanner = scanner_service # El servicio de escaneo de red
        self.port_scanner = PortScanner() # Nuevo servicio de escaneo de puertos
        self.main_page = page
        self.notification_service = notification_service
        self.visible = False
        
        # Almacenamiento de dispositivos
        self.all_devices = []
        self.selected_ips = set() # IPs seleccionadas para port scan
        self.device_alerts_enabled = True

        # 1. Crear la tabla (ahora con columa de selección)
        self.table = create_device_table()

        # 2. Controles de Network Scan
        self.btn_scan_network = ft.Button(
            "Scan Network",
            icon=ft.Icons.RADAR,
            on_click=self.run_scan,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white"
        )
        
        self.search_field = ft.TextField(
            hint_text="Search by IP, MAC or Vendor...",
            on_change=self.apply_filter,
            prefix_icon=ft.Icons.SEARCH,
            expand=True,
            height=40,
            text_size=14,
            content_padding=10
        )
        
        self.clear_btn = ft.IconButton(
            icon=ft.Icons.CLEAR,
            on_click=self.clear_filter,
            tooltip="Clear filter"
        )

        # 3. Controles de Port Scan
        self.mode_dropdown = ft.Dropdown(
            width=150,
            options=[
                ft.dropdown.Option(ScanMode.QUICK.value, "Quick (Top 20)"),
                ft.dropdown.Option(ScanMode.STANDARD.value, "Standard (Top 100)"),
                ft.dropdown.Option(ScanMode.FULL.value, "Full (1-1024)"),
            ],
            value=ScanMode.QUICK.value,
            label="Scan Mode",
            text_size=12,
            height=45,
            content_padding=10
        )
        
        self.btn_scan_ports = ft.ElevatedButton(
            "Scan Ports",
            icon=ft.Icons.SECURITY,
            on_click=self.run_port_scan,
            bgcolor=ft.Colors.ORANGE_900,
            color="white",
            disabled=True # Se habilita al seleccionar dispositivos
        )

        # 4. Resultados de Port Scan (Dialog)
        self.results_dialog = ft.AlertDialog(
            title=ft.Text("Port Scan Results"),
            content=ft.Text("Scanning..."),
            actions=[
                ft.TextButton("Close", on_click=lambda e: self.close_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # 5. Armar el Layout
        self.controls = [
            ft.Text("Network & Port Scanner", size=24, weight="bold"),
            
            # Sección Network Scan
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Network Discovery", size=16, weight="bold"),
                        self.btn_scan_network
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.only(bottom=10)
            ),
            
            # Filtros
            ft.Row([self.search_field, self.clear_btn]),
            
            ft.Divider(),
            
            # Sección Port Scan
            ft.Container(
                content=ft.Row(
                    [
                        ft.Row([
                            ft.Icon(ft.Icons.SECURITY, size=20, color=ft.Colors.ORANGE),
                            ft.Text("Port Scanner Actions:", weight="bold"),
                        ]),
                        ft.Row([
                            self.mode_dropdown,
                            self.btn_scan_ports
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                bgcolor=ft.Colors.BLACK_26,
                padding=10,
                border_radius=5
            ),
            
            ft.Container(height=10),
            
            # Tabla
            ft.Column([self.table], scroll=ft.ScrollMode.AUTO, expand=True)
        ]
        self.expand = True

    async def run_scan(self, e):
        """Ejecuta escaneo de red."""
        self.btn_scan_network.disabled = True
        self.btn_scan_network.text = "Scanning..."
        self.main_page.update()

        try:
            devices = await asyncio.to_thread(self.scanner.scan_network)
            
            # Notificaciones
            if self.notification_service and self.device_alerts_enabled:
                new_devices = self.scanner.detect_new_devices(devices)
                for device in new_devices:
                    self.notification_service.notify_new_device(device)
            
            self.all_devices = devices
            self._update_table(devices)
            
        except Exception as ex:
            print(f"Error scanning: {ex}")
        
        self.btn_scan_network.disabled = False
        self.btn_scan_network.text = "Scan Network"
        self.main_page.update()
    
    def _on_checkbox_change(self, e, ip):
        """Maneja selección de dispositivos."""
        if e.control.value:
            self.selected_ips.add(ip)
        else:
            self.selected_ips.discard(ip)
        
        # Habilitar botón si hay seleccionados
        self.btn_scan_ports.disabled = len(self.selected_ips) == 0
        self.btn_scan_ports.text = f"Scan Ports ({len(self.selected_ips)})"
        self.main_page.update()

    def _update_table(self, devices):
        """Actualiza la tabla con los dispositivos."""
        self.table.rows.clear()
        
        for dev in devices:
            ip = dev['ip']
            is_selected = ip in self.selected_ips
            
            self.table.rows.append(
                ft.DataRow(cells=[
                    # Checkbox Cell
                    ft.DataCell(
                        ft.Checkbox(
                            value=is_selected,
                            on_change=lambda e, x=ip: self._on_checkbox_change(e, x)
                        )
                    ),
                    ft.DataCell(ft.Text(ip)),
                    ft.DataCell(ft.Text(dev['mac'], font_family="Consolas")),
                    ft.DataCell(ft.Text(dev.get('vendor', 'Unknown'), size=12)),
                    ft.DataCell(ft.Icon(ft.Icons.CIRCLE, color="green", size=10)),
                ])
            )
        self.main_page.update()

    def apply_filter(self, e):
        """Filtra dispositivos."""
        if not self.all_devices: return
        
        text = self.search_field.value.lower().strip()
        filtered = [
            d for d in self.all_devices 
            if not text or 
            text in d.get('ip', '').lower() or 
            text in d.get('mac', '').lower() or 
            text in d.get('vendor', '').lower()
        ]
        self._update_table(filtered)

    def clear_filter(self, e):
        self.search_field.value = ""
        self._update_table(self.all_devices)

    async def run_port_scan(self, e):
        """Ejecuta escaneo de puertos en dispositivos seleccionados."""
        if not self.selected_ips: return
        
        mode = ScanMode(self.mode_dropdown.value)
        
        # Abrir diálogo
        self.main_page.dialog = self.results_dialog
        self.results_dialog.open = True
        self.results_dialog.content = ft.Column([
            ft.ProgressRing(), 
            ft.Text(f"Scanning {len(self.selected_ips)} devices ({mode.value} mode)...")
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, height=100)
        self.main_page.update()
        
        # Ejecutar escaneos
        results_ui = []
        
        for ip in self.selected_ips:
            try:
                # Escanear puertos (async call to thread)
                open_ports = await asyncio.to_thread(self.port_scanner.scan, ip, mode)
                
                # Crear UI para este dispositivo
                device_results = ft.Column([
                    ft.Text(f"Device: {ip}", weight="bold", size=16, color=ft.Colors.CYAN),
                    ft.Divider(),
                ])
                
                if open_ports:
                    # Tabla de puertos
                    dt = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Port")),
                            ft.DataColumn(ft.Text("Service")),
                            ft.DataColumn(ft.Text("State")),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(str(p["port"]))),
                                ft.DataCell(ft.Text(p["service"])),
                                ft.DataCell(ft.Text(p["state"], color="green")),
                            ]) for p in open_ports
                        ],
                        heading_row_height=30,
                        data_row_min_height=30,
                    )
                    device_results.controls.append(dt)
                else:
                    device_results.controls.append(ft.Text("No open ports found.", italic=True))
                
                device_results.controls.append(ft.Container(height=20))
                results_ui.append(device_results)
                
            except Exception as ex:
                results_ui.append(ft.Text(f"Error scanning {ip}: {ex}", color="red"))

        # Actualizar contenido del diálogo
        self.results_dialog.content = ft.Column(
            results_ui, 
            scroll=ft.ScrollMode.AUTO, 
            height=400, 
            width=500
        )
        self.main_page.update()

    def close_dialog(self):
        self.results_dialog.open = False
        self.main_page.update()
