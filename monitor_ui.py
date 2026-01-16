import flet as ft
import flet_charts as fch
import psutil
import asyncio
import math

def convertir_bytes(tamanio):
    """Convierte bytes a KB, MB, GB para el texto superior."""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanio < 1024:
            return f"{tamanio:.2f} {unidad}"
        tamanio /= 1024

async def main(page: ft.Page):
    # --- CONFIGURACIÓN ---
    page.title = "Monitor de Red 2026 - Versión Final"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 800
    page.window_height = 600
    page.padding = 20

    # --- DATOS ---
    datos_bajada = [fch.LineChartDataPoint(i, 0) for i in range(60)]
    datos_subida = [fch.LineChartDataPoint(i, 0) for i in range(60)]

    # Texto Grande: Aquí es donde leeremos los valores exactos con unidades
    lbl_velocidad = ft.Text("Sensores listos.", size=25, weight="bold", font_family="Consolas")

    # --- SERIES ---
    serie_bajada = fch.LineChartData(
        points=datos_bajada,
        stroke_width=2,
        color=ft.Colors.GREEN_400,
        curved=False # False para precisión técnica (evita que baje de 0)
    )

    serie_subida = fch.LineChartData(
        points=datos_subida,
        stroke_width=2,
        color=ft.Colors.CYAN_400,
        curved=False
    )

    # --- GRÁFICO ---
    # Eliminamos cualquier configuración de tooltip para evitar errores de versión.
    chart = fch.LineChart(
        data_series=[serie_bajada, serie_subida],
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

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.NETWORK_CHECK, color="green", size=30),
                    ft.Text("MONITOR DE RED - FINAL", size=22, weight="bold")
                ]),
                # El valor numérico principal
                ft.Container(lbl_velocidad, padding=5),
                
                # El gráfico de tendencias
                ft.Container(
                    chart, 
                    height=400, 
                    padding=10, 
                    border_radius=10, 
                    bgcolor=ft.Colors.BLACK12
                ),
                ft.Text("Referencia: Eje izquierdo en MB/s fijos.", size=12, color="grey")
            ]),
            padding=10
        )
    )

    # --- LÓGICA ---
    async def loop_monitoreo():
        io_inicial = psutil.net_io_counters()
        bytes_enviados_ant = io_inicial.bytes_sent
        bytes_recibidos_ant = io_inicial.bytes_recv
        
        while True:
            await asyncio.sleep(1)

            io_actual = psutil.net_io_counters()
            subida = io_actual.bytes_sent - bytes_enviados_ant
            bajada = io_actual.bytes_recv - bytes_recibidos_ant

            # Convertimos a MB para el dibujo del gráfico
            subida_mb = subida / 1048576 
            bajada_mb = bajada / 1048576

            # Actualizamos el texto superior (Aquí es donde ves los KB/MB bonitos)
            lbl_velocidad.value = f"⬇️ {convertir_bytes(bajada)}/s   ⬆️ {convertir_bytes(subida)}/s"

            # Lógica de datos (FIFO)
            datos_bajada.pop(0)
            datos_subida.pop(0)
            datos_bajada.append(fch.LineChartDataPoint(59, bajada_mb))
            datos_subida.append(fch.LineChartDataPoint(59, subida_mb))

            for i, punto in enumerate(datos_bajada):
                punto.x = i
            for i, punto in enumerate(datos_subida):
                punto.x = i

            # Escala Fija de Bloques (Estabilidad Visual)
            max_val = max(bajada_mb, subida_mb)
            
            if max_val < 10:
                chart.max_y = 10
            else:
                chart.max_y = (math.ceil(max_val / 2.5) * 2.5) + 2.5 

            page.update()

            bytes_enviados_ant = io_actual.bytes_sent
            bytes_recibidos_ant = io_actual.bytes_recv

    await loop_monitoreo()

ft.app(target=main)