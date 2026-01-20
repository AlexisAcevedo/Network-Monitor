import flet as ft

def setup_page (page: ft.Page):
    """Configuracion basica de la ventana"""
    page.title = "Network Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0

def create_app_shell(sidebar, content_area):
    """
    Crea el layout principal usando una Fila (Row)
    [ Sidebar | Linea divisoria | Area de contenido ]
    """
    return ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color="grey"),
            ft.Container(
                content=content_area,
                expand=True,
                padding=20
            )
        ],
        expand=True
    )