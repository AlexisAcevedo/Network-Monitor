import flet as ft

def MonitorView(chart, speed_label, stats_panel):
    """
    Crea la vista del Monitor de trafico.
    Recibe los componentes ya creados (chart, label y stats) para organizarlos visualmente
    """
    return ft.Column(
        [
            ft.Text("Real-Time traffic", size=20, weight="bold"),

            # Contenedor para el texto de velocidad 
            ft.Container(speed_label, padding=ft.padding.only(bottom=10)),

            # Contenedor del grafico con fondo oscuro
            ft.Container(
                content=chart,
                height=350,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLACK_12
            ),
            
            # Panel de estadísticas
            ft.Container(
                content=stats_panel,
                padding=ft.padding.only(top=20)
            ),
        ],
        visible=True # Esta vista arranca visible
    )


def create_stats_panel():
    """
    Crea el panel de estadísticas con 4 métricas.
    Retorna el panel y los controles de texto para actualizar.
    """
    # Textos que se actualizarán
    peak_text = ft.Text("Peak: -- MB/s", size=14, weight="w500")
    total_text = ft.Text("Total: -- MB", size=14, weight="w500")
    avg_text = ft.Text("Avg: -- MB/s", size=14, weight="w500")
    
    # Panel con 3 columnas de estadísticas
    panel = ft.Row(
        [
            # Columna 1: Pico
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.TRENDING_UP, color=ft.Colors.ORANGE, size=24),
                    peak_text
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                border_radius=8,
                bgcolor=ft.Colors.BLACK_12,
                expand=True
            ),
            
            # Columna 2: Total
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.DATA_USAGE, color=ft.Colors.BLUE, size=24),
                    total_text
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                border_radius=8,
                bgcolor=ft.Colors.BLACK_12,
                expand=True
            ),
            
            # Columna 3: Promedio
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.GREEN, size=24),
                    avg_text
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=15,
                border_radius=8,
                bgcolor=ft.Colors.BLACK_12,
                expand=True
            ),
        ],
        spacing=10
    )
    
    return panel, peak_text, total_text, avg_text
