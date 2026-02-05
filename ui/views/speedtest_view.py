"""
Vista de Speedtest para mostrar resultados de velocidad de internet.
"""

import flet as ft
import asyncio
from core.speedtest_service import SpeedtestService


def SpeedtestView(page: ft.Page):
    """
    Crea la vista de Speedtest.
    Muestra 3 cards con Download, Upload y Ping.
    """
    # Servicio de speedtest
    speedtest_service = SpeedtestService()
    
    # Estados
    is_running = False
    
    # Componentes de resultado
    download_value = ft.Text("--", size=48, weight="bold", color=ft.Colors.CYAN)
    download_unit = ft.Text("Mbps", size=16, color=ft.Colors.CYAN_200)
    
    upload_value = ft.Text("--", size=48, weight="bold", color=ft.Colors.PURPLE)
    upload_unit = ft.Text("Mbps", size=16, color=ft.Colors.PURPLE_200)
    
    ping_value = ft.Text("--", size=48, weight="bold", color=ft.Colors.GREEN)
    ping_unit = ft.Text("ms", size=16, color=ft.Colors.GREEN_200)
    
    server_text = ft.Text("Server: --", size=12, color=ft.Colors.WHITE54)
    status_text = ft.Text("Ready to test", size=14, color=ft.Colors.WHITE70)
    
    # Loading indicator
    progress_ring = ft.ProgressRing(visible=False, width=24, height=24)
    
    # Botón de test
    run_button = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.SPEED), ft.Text("Run Test")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        ),
        on_click=None,  # Se asigna después
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            padding=20
        ),
        width=200
    )
    
    async def run_speedtest(e):
        nonlocal is_running
        
        if is_running:
            return
        
        is_running = True
        
        # UI: Mostrar loading
        run_button.disabled = True
        progress_ring.visible = True
        status_text.value = "Finding best server..."
        status_text.color = ft.Colors.AMBER
        download_value.value = "--"
        upload_value.value = "--"
        ping_value.value = "--"
        server_text.value = "Server: Testing..."
        page.update()
        
        # Ejecutar test en thread separado
        try:
            status_text.value = "Testing download speed..."
            page.update()
            
            # Ejecutar en executor para no bloquear UI
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, speedtest_service.run_test)
            
            if result["error"]:
                status_text.value = f"Error: {result.get('error_message', 'Unknown error')}"
                status_text.color = ft.Colors.RED
            else:
                # Actualizar valores
                download_value.value = f"{result['download_mbps']:.1f}"
                upload_value.value = f"{result['upload_mbps']:.1f}"
                ping_value.value = f"{result['ping_ms']:.0f}"
                server_text.value = f"Server: {result['server_name']}"
                status_text.value = "Test completed!"
                status_text.color = ft.Colors.GREEN
                
        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            status_text.color = ft.Colors.RED
        finally:
            is_running = False
            run_button.disabled = False
            progress_ring.visible = False
            page.update()
    
    run_button.on_click = run_speedtest
    
    # Cards de resultados
    def create_result_card(icon, title, value_text, unit_text, bg_color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=32, color=ft.Colors.WHITE70),
                    ft.Text(title, size=14, color=ft.Colors.WHITE54),
                    ft.Row(
                        [value_text, unit_text],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        spacing=5
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            padding=20,
            border_radius=12,
            bgcolor=bg_color,
            expand=True
        )
    
    download_card = create_result_card(
        ft.Icons.DOWNLOAD, "DOWNLOAD", download_value, download_unit, ft.Colors.BLACK_26
    )
    upload_card = create_result_card(
        ft.Icons.UPLOAD, "UPLOAD", upload_value, upload_unit, ft.Colors.BLACK_26
    )
    ping_card = create_result_card(
        ft.Icons.NETWORK_PING, "PING", ping_value, ping_unit, ft.Colors.BLACK_26
    )
    
    # Layout principal
    return ft.Column(
        [
            ft.Text("Internet Speed Test", size=24, weight="bold"),
            ft.Text("Test your connection speed", size=14, color=ft.Colors.WHITE54),
            
            # Espacio
            ft.Container(height=20),
            
            # Cards de resultados
            ft.Row(
                [download_card, upload_card, ping_card],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
            # Espacio
            ft.Container(height=20),
            
            # Botón y status
            ft.Row(
                [run_button, progress_ring],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(
                content=status_text,
                padding=ft.padding.only(top=10)
            ),
            
            # Server info
            ft.Container(
                content=server_text,
                padding=ft.padding.only(top=20)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        visible=False  # Arranca oculta, se muestra al navegar
    )
