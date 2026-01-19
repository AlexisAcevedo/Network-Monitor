import psutil
import psutil
class NetworkSensor:
    def __init__(self):
        # T0 Lectura inicial para referencia
        self.io_prev = psutil.net_io_counters()

    def get_traffic(self):
        """
        Retorna una tupla: (download_mb, upload_mb)
        calculada desde la ultima vez que se llamó
        """

        io_current = psutil.net_io_counters()

        # Diferencia (bytes actuales - bytes anteriores)
        upload = io_current.bytes_sent - self.io_prev.bytes_sent
        download = io_current.bytes_recv - self.io_prev.bytes_recv

        # Actualizamos referencia para la proxima vuelta
        self.io_prev = io_current

        # Convertimos a MB (1MB = 1048576)
        return (download / 1048576, upload / 1048576)

    def format_bytes(self, bytes_raw):
        """Convierte bytes crudos a KB, MB, GB para mostrar en pantalla"""
        size = bytes_raw
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /=1024
        return f"{size:.2f} PB"