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
        
        # 3. ESTADÍSTICAS DE TRÁFICO
        self.peak_download = 0.0
        self.peak_upload = 0.0
        self.total_download = 0.0
        self.total_upload = 0.0
        self.sample_count = 0
        
        # 4. CONFIGURACIÓN DE ALERTAS DE TRÁFICO ALTO
        self.traffic_threshold_mb = 10.0  # Umbral por defecto: 10 MB/s
        self.high_traffic_alerts_enabled = False  # Deshabilitado por defecto

    def update_traffic(self, download_mb, upload_mb):
        """
        Actualiza los datos usando reciclaje de objetos (Cero impacto en RAM).
        """
        # A) Guardamos el dato numérico crudo
        self.download_values.append(download_mb)
        self.upload_values.append(upload_mb)

        # B) Actualizamos los objetos gráficos existentes
        for i in range(60):
            self.download_points[i].y = self.download_values[i]
            self.upload_points[i].y = self.upload_values[i]
        
        # C) Actualizar estadísticas
        # Actualizar picos
        if download_mb > self.peak_download:
            self.peak_download = download_mb
        if upload_mb > self.peak_upload:
            self.peak_upload = upload_mb
        
        # Acumular totales
        self.total_download += download_mb
        self.total_upload += upload_mb
        
        # Incrementar contador de muestras
        self.sample_count += 1

    def calculate_dynamic_scale(self, current_down, current_up):
        """
        Calcula el eje Y del gráfico de forma dinámica.
        Retorna un valor redondeado hacia arriba para que se vea limpio.
        """
        max_value = max(current_down, current_up, 1)
        return math.ceil(max_value * 1.2)  # 20% de margen superior
    
    def get_stats(self) -> dict:
        """
        Retorna un diccionario con todas las estadísticas de tráfico.
        
        Returns:
            Diccionario con peak, total y avg para download y upload
        """
        # Calcular promedios
        avg_download = self.total_download / self.sample_count if self.sample_count > 0 else 0.0
        avg_upload = self.total_upload / self.sample_count if self.sample_count > 0 else 0.0
        
        return {
            "peak_download": self.peak_download,
            "peak_upload": self.peak_upload,
            "total_download": self.total_download,
            "total_upload": self.total_upload,
            "avg_download": avg_download,
            "avg_upload": avg_upload
        }
    
    def reset_stats(self):
        """Reinicia todas las estadísticas a cero."""
        self.peak_download = 0.0
        self.peak_upload = 0.0
        self.total_download = 0.0
        self.total_upload = 0.0
        self.sample_count = 0
    
    def set_traffic_threshold(self, threshold_mb: float):
        """
        Configura el umbral de tráfico alto.
        
        Args:
            threshold_mb: Umbral en MB/s
        """
        self.traffic_threshold_mb = max(0.1, threshold_mb)  # Mínimo 0.1 MB/s
    
    def check_high_traffic(self, download_mb: float, upload_mb: float) -> bool:
        """
        Verifica si el tráfico actual supera el umbral configurado.
        
        Args:
            download_mb: Tráfico de descarga en MB/s
            upload_mb: Tráfico de subida en MB/s
            
        Returns:
            True si alguno de los dos supera el umbral
        """
        if not self.high_traffic_alerts_enabled:
            return False
        
        return download_mb > self.traffic_threshold_mb or upload_mb > self.traffic_threshold_mb