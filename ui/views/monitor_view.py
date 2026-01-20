import flet as ft

def MonitorView(chart, speed_label):
    """
    Crea la vista del Monitor de trafico.
    Recibe los componentes ya creados (chart y label) para organizarlos visualmente
    """
    return ft.Column(
        [
            ft.Text("Real-Time traffic", size=20, weight="bold"),

            # Contenedor para el texto de velocidad 
            ft.Container(speed_label, padding=ft.padding.only(bottom=20)),

            # Contenedor del grafico con fondo oscuro
            ft.Container(
                content=chart,
                height=400,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLACK_12
            ),
        ],
        visible=True # Esta vista arranca visible
    )