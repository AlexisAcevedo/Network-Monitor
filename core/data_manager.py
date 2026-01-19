import math
import flet_charts as fch
from collections import deque

class DataManager:
    def __init__(self):
        # 1. POOL DE OBJETOS GRÁFICOS (UI)
        # Creamos los 60 puntos UNA sola vez al inicio.
        self.download_points = [fch.LineChartDataPoint(i, 0) for i in range(60)]
        self.upload_points = [fch.LineChartDataPoint(i, 0) for i in range(60)]

        # 2. BUFFER DE DATOS CRUDOS (Memoria optimizada)
        # Usamos deque para que los datos viejos se borren solos.
        self.download_values = deque([0]*60, maxlen=60)
        self.upload_values = deque([0]*60, maxlen=60)

    def update_traffic(self, download_mb, upload_mb):
        """
        Actualiza los datos usando reciclaje de objetos (Cero impacto en RAM).
        """
        # A) Guardamos el dato numérico crudo
        self.download_values.append(download_mb)
        self.upload_values.append(upload_mb)

        # B) Inyectamos ese valor en el punto gráfico correspondiente
        # 'zip' nos permite recorrer la lista de puntos y la cola de valores a la par
        for point, value in zip(self.download_points, self.download_values):
            point.y = value

        for point, value in zip(self.upload_points, self.upload_values):
            point.y = value

    def calculate_dynamic_scale(self, download_mb, upload_mb):
        """
        Calcula el techo del gráfico.
        - Piso mínimo: 100 MB.
        - Crecimiento: Bloques de 5 MB.
        """
        # Buscamos el pico más alto en todo el historial actual (los 60 segundos)
        # Esto evita que la escala salte bruscamente si el pico dura solo 1 segundo.
        max_val = max(max(self.download_values), max(self.upload_values))
        
        # Lógica de escala
        if max_val < 100:
            return 100
        else:
            # Si pasamos los 100 MB, subimos de a 5 en 5.
            # Ejemplo: 102 MB -> Techo 110 MB (105 + 5 de margen)
            return (math.ceil(max_val / 5) * 5) + 5