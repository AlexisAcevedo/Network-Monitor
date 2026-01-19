import math
import flet_charts as fch

class DataManager:
    def __init__(self):
        # Inicializamos listas con 60 puntos en 0 (Download/Upload)
        self.download_points = [fch.LineChartDataPoint(i, 0) for i in range(60)]
        self.upload_points = [fch.LineChartDataPoint(i, 0) for i in range(60)]

    def update_traffic(self, download_mb, upload_mb):
            """Aplica lógica FIFO (ventana deslizante) y actualiza las listas"""
            # 1. Eliminar dato viejo
            self.download_points.pop(0)
            self.upload_points.pop(0)

            # 2. Agregar dato nuevo (temporalmente en indice 59)
            self.download_points.append(fch.LineChartDataPoint(59, download_mb))
            self.upload_points.append(fch.LineChartDataPoint(59, upload_mb))

            # 3. Re indexar eje X (0 a 59)
            for i in range(60):
                self.download_points[i].x = i
                self.upload_points[i].x = i

    def calculate_dynamic_scale(self, download_mb, upload_mb):
            """Calcula el techo del grafico basandose en bloques de 2.5MB"""
            max_val = max(download_mb, upload_mb)

            if max_val < 10:
                return 10
            else:
                # Matematica para encontrar el proximo multiplo de 2.5
                return (math.ceil(max_val / 2.5) * 2.5) + 2.5