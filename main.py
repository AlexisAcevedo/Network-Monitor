import flet as ft
import asyncio

from core.sensor import NetworkSensor
from core.data_manager import DataManager
from ui.layout import setup_page, create_main_layout
from ui.charts import create_network_chart

async def main(page: ft.Page):
    # 1. Configuración Visual
    setup_page(page)
    
    # 2. Inicialización de logica
    sensor = NetworkSensor()
    data_manager = DataManager()

    # 3. Creación de UI
    # Conectamos las listas del Manager al Gráfico
    chart = create_network_chart(data_manager.download_points, data_manager.upload_points)
    
    speed_label = ft.Text("Initializing sensors...", size=25, weight="bold", font_family="Consolas")

    # Ensamblamos la pantalla
    layout = create_main_layout(chart, speed_label)
    page.add(layout)

    # 4. Bucle Principal (Controlador)
    while True:
        await asyncio.sleep(1)

        # A) Obtener datos crudos (MB)
        download_mb, upload_mb = sensor.get_traffic()

        # B) Procesar datos (Actualizar listas y calcular escala)
        data_manager.update_traffic(download_mb, upload_mb)
        new_scale = data_manager.calculate_dynamic_scale(download_mb, upload_mb)

        # C) Actualizar UI
        
        # Texto: Reconvertimos a bytes para usar el formateador bonito
        bytes_download = download_mb * 1048576
        bytes_upload = upload_mb * 1048576
        
        speed_label.value = (
            f"⬇️ {sensor.format_bytes(bytes_download)}/s   "
            f"⬆️ {sensor.format_bytes(bytes_upload)}/s"
        )
        
        # Gráfico: Solo tocamos la escala, los puntos ya se actualizaron en el paso B
        chart.max_y = new_scale
        
        page.update()


ft.run(main)