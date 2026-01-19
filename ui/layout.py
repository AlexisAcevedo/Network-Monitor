import flet as ft

def setup_page(page: ft.Page):
    """Cofiguracion global de la ventana"""
    page.title = "Network Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.width = 800
    page.height = 600
    page.padding = 20

def create_main_layout(chart, speed_label):
    """
    Ensambla la pantalla principal.
    Recibe los widgets activos (chart y label) y los coloca en el diseño
    """

    # Encabezado
    header = ft.Row(
        [
            ft.Icon(ft.Icons.NETWORK_CHECK, color ="green", size=30),
            ft.Text("NETWORK MONITOR", size=22, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.START
    )

    # Contenedor principal
    layout = ft.Container(
        content=ft.Column(
            [
                header,
                # Espacio para el texto de velocidad
                ft.Container(speed_label, padding=5),
                # Espacio para el grafico
                ft.Container(
                    content=chart,
                    height=400,
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.Colors.BLACK_12
                ),
                ft.Text("Status: Modular System Active | Scale: 2.5MB Fixed", size=12, color="grey")
            ],
            spacing=10
        ),
        padding=10,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        border_radius=15
    )

    return layout