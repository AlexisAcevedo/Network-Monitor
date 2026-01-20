import asyncio
import flet as ft
import asyncio
from ui.device_list import create_device_table

class ScannerView(ft.Column):
    def __init__(self, scanner_service, page: ft.Page):
        super().__init__()
        self.scanner = scanner_service # El servicio de escaneo
        self.main_page = page
        self.visible = False # Esta vista arranca oculta

        # 1. Crear la tabla
        self.table = create_device_table()

        # 2. Crear el boton
        self.btn = ft.Button(
            "Scan Network",
            icon=ft.Icons.RADAR,
            on_click=self.run_scan,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color="white"
        )

        # 3. Armar el Layout (lo que se ve en pantalla)
        self.controls = [
            ft.Text("Network Device Scanner", size=20, weight="bold"),
            
            # Fila con descripción a la izq y botón a la der
            ft.Row(
                [ft.Text("Detect connected devices via ARP Protocol"), self.btn], 
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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

            # C) Llenar la tabla con resultados
            self.table.rows.clear()
            for dev in devices:
                self.table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(dev['ip'])),
                        ft.DataCell(ft.Text(dev['mac'], font_family="Consolas")),
                        ft.DataCell(ft.Icon(ft.Icons.CIRCLE, color="green", size=10)),
                    ])
                )
        except Exception as e:
            print(f"Error scanning: {e}")

        # D) Restaurar boton
        self.btn.disabled=False
        self.btn.text = "Scan network"
        self.btn.icon = ft.Icons.RADAR
        self.main_page.update()
