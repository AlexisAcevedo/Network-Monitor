import flet as ft

def create_sidebar(on_nav_change):
    """
    Crea la barra lateral de navegacion

    Args:
        on_nav_change (function): Funcion que se ejecuta al cambiar de pestaña
    """
    return ft.NavigationRail(
        selected_index=0, # Por defecto arranca en el primero (Monitor)
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        bgcolor=ft.Colors.BLACK_26,
        group_alignment=-0.9,
        destinations=[
            # Opcion 0: Monitor
            ft.NavigationRailDestination(
                icon=ft.Icons.TIMELAPSE,
                selected_icon=ft.Icons.TIMELAPSE_SHARP,
                label="Monitor"
            ),
            # Opcion 1: Dispositivos
            ft.NavigationRailDestination(
                icon=ft.Icons.DEVICES_OTHER,
                selected_icon=ft.Icons.DEVICES,
                label="Devices"
            ),
        ],
        on_change=on_nav_change # Aca se conecta la logica
    )