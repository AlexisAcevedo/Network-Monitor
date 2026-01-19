import flet as ft
import flet_charts as fch

def create_network_chart(download_data, upload_data):
    """Crea el objeto LineChart enlazado a la lista de datos"""

    # Serie 1: Download (verde)
    download_series = fch.LineChartData(
        points=download_data,
        stroke_width=2,
        color=ft.Colors.GREEN_400,
        curved=False
    )

    # Serie 2: Upload (Cian)
    upload_series = fch.LineChartData(
        points=upload_data,
        stroke_width=2,
        color=ft.Colors.CYAN_400,
        curved=False
    )

    # Configuracion del Chart
    chart = fch.LineChart(
        data_series=[download_series, upload_series],
        border=ft.Border.all(1, ft.Colors.GREY_800),
        left_axis=fch.ChartAxis(
            label_size=40,
            title=ft.Text("MB/s", size=10, weight="bold"),
            show_labels=True,
        ),
        bottom_axis=fch.ChartAxis(
            label_size=0,
            show_labels=False
        ),
        min_y=0,
        max_y=10,
        expand=True,
    )

    return chart