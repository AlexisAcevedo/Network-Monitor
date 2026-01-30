import flet as ft

def create_device_table():
    """
    Retorna el objeto DataTable configurado (Columnas y estilos),
    pero sin filas de datos iniciales
    """
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("IP Adress", weight="bold", color="white")),
            ft.DataColumn(ft.Text("MAC Address", weight="bold", color="cyan")),
            ft.DataColumn(ft.Text("Vendor", weight="bold", color="orange")),
            ft.DataColumn(ft.Text("Status", weight="bold")),
        ],
        rows=[], # Inicia vacia
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        heading_row_color=ft.Colors.BLACK_45,
        heading_row_height=40,
        data_row_min_height=40,
        expand=True # Expande para ocupar el ancho disponible
    )