import flet as ft
import asyncio

# --- 1. SERVICIOS (BACKEND) ---
from core.sensor import NetworkSensor
from core.data_manager import DataManager
from core.scanner import NetworkScanner
from core.notification_service import NotificationService

# --- 2. COMPONENTES UI ---
from ui.layout import setup_page, create_app_shell
from ui.sidebar import create_sidebar
from ui.charts import create_network_chart

# --- 3. VISTAS (PANTALLAS) ---
from ui.views.monitor_view import MonitorView, create_stats_panel, create_alerts_config
from ui.views.scanner_view import ScannerView
from ui.views.speedtest_view import SpeedtestView
from ui.views.topology_view import TopologyView

async def main(page: ft.Page):
    # A) Configuración inicial
    setup_page(page)
    
    # B) Instanciar Backend
    sensor = NetworkSensor()
    data_manager = DataManager()
    scanner_service = NetworkScanner()
    notification_service = NotificationService()

    # C) Preparar componentes para la Vista Monitor
    # (El gráfico vive en el main para que podamos actualizarlo en el bucle)
    chart = create_network_chart(data_manager.download_points, data_manager.upload_points)
    speed_label = ft.Text("Initializing...", size=30, weight="bold", font_family="Consolas")
    stats_panel, peak_text, total_text, avg_text = create_stats_panel()
    alerts_config, alerts_toggle, threshold_field = create_alerts_config(data_manager)

    # D) Instanciar las Vistas
    # Vista 1: Monitor
    view_monitor = MonitorView(chart, speed_label, stats_panel, alerts_config)
    
    # Vista 2: Escáner
    view_scanner = ScannerView(scanner_service, page, notification_service)
    
    # Vista 3: Topología (Nueva)
    # Vista 3: Topología (Nueva)
    view_topology, refresh_topology = TopologyView(scanner_service, page)
    
    # Vista 4: Speedtest
    view_speedtest = SpeedtestView(page)

    # E) Lógica de Navegación
    async def nav_change(e):
        index = e.control.selected_index
        # Simplemente prendemos y apagamos la visibilidad
        view_monitor.visible = (index == 0)
        view_scanner.visible = (index == 1)
        view_topology.visible = (index == 2)
        view_speedtest.visible = (index == 3)
        
        # Si entramos a la vista de escáner, ejecutar escaneo automático
        if index == 1:
            await view_scanner.run_scan(None)
            
        # Si entramos a topología, cargar topología autmáticamente
        if index == 2:
            refresh_topology()
        
        page.update()

    # Crear el menú lateral
    sidebar = create_sidebar(nav_change)

    # F) Ensamblaje Final
    # Metemos las cuatro vistas en el área de contenido.
    content_area = ft.Column([view_monitor, view_scanner, view_topology, view_speedtest])
    
    layout = create_app_shell(sidebar, content_area)
    page.add(layout)

    # G) Bucle Principal (Ciclo de Vida)
    while True:
        await asyncio.sleep(1)
        
        # 1. Obtener datos nuevos
        down, up = sensor.get_traffic()
        data_manager.update_traffic(down, up)
        
        # 2. Actualizar UI (Solo si estamos viendo el monitor)
        # Esto ahorra recursos, aunque calculamos los datos igual para no perder historial
        if view_monitor.visible:
            new_scale = data_manager.calculate_dynamic_scale(down, up)
            bytes_down = down * 1048576
            bytes_up = up * 1048576
            
            # Actualizamos textos y gráfico
            speed_label.value = f"⬇️ {sensor.format_bytes(bytes_down)}/s   ⬆️ {sensor.format_bytes(bytes_up)}/s"
            chart.max_y = new_scale
            
            # Actualizar estadísticas
            stats = data_manager.get_stats()
            peak_text.value = f"Peak: {stats['peak_download']:.2f} MB/s ⬇️ | {stats['peak_upload']:.2f} MB/s ⬆️"
            total_text.value = f"Total: {stats['total_download']:.2f} MB ⬇️ | {stats['total_upload']:.2f} MB ⬆️"
            avg_text.value = f"Avg: {stats['avg_download']:.2f} MB/s ⬇️ | {stats['avg_upload']:.2f} MB ⬆️"
            
            # Verificar tráfico alto y notificar
            if data_manager.check_high_traffic(down, up):
                max_traffic = max(down, up)
                notification_service.notify_high_traffic(max_traffic, data_manager.traffic_threshold_mb)
            
            page.update()

ft.run(main)