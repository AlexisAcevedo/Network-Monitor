"""
Servicio de notificaciones para Windows usando winotify.
"""

import time
from winotify import Notification, audio


class NotificationService:
    """
    Servicio para mostrar notificaciones nativas de Windows.
    Incluye cooldown para evitar spam de notificaciones.
    """
    
    def __init__(self):
        """Inicializa el servicio de notificaciones."""
        self.last_notification_time = {}
        self.cooldown_seconds = 30  # Cooldown de 30 segundos entre notificaciones del mismo tipo
    
    def notify(self, title: str, message: str, icon_path: str = None, notification_type: str = "general"):
        """
        Muestra una notificación de Windows.
        
        Args:
            title: Título de la notificación
            message: Mensaje de la notificación
            icon_path: Ruta al ícono (opcional)
            notification_type: Tipo de notificación para cooldown
            
        Returns:
            True si se mostró la notificación, False si está en cooldown
        """
        # Verificar cooldown
        current_time = time.time()
        last_time = self.last_notification_time.get(notification_type, 0)
        
        if current_time - last_time < self.cooldown_seconds:
            # Aún en cooldown, no mostrar notificación
            return False
        
        # Mostrar notificación
        try:
            toast = Notification(
                app_id="Network Monitor",
                title=title,
                msg=message,
                duration="short"
            )
            
            # Añadir sonido
            toast.set_audio(audio.Default, loop=False)
            
            # Mostrar
            toast.show()
            
            # Actualizar timestamp del último notification
            self.last_notification_time[notification_type] = current_time
            return True
            
        except Exception as e:
            print(f"Error mostrando notificación: {e}")
            return False
    
    def notify_new_device(self, device: dict):
        """
        Notifica sobre un nuevo dispositivo detectado.
        
        Args:
            device: Diccionario con información del dispositivo (ip, mac, vendor)
        """
        ip = device.get('ip', 'Unknown')
        vendor = device.get('vendor', 'Unknown')
        mac = device.get('mac', 'Unknown')
        
        title = "🔔 New Device Detected"
        message = f"IP: {ip}\nVendor: {vendor}\nMAC: {mac}"
        
        return self.notify(title, message, notification_type=f"new_device_{ip}")
    
    def notify_high_traffic(self, current_mb: float, threshold_mb: float):
        """
        Notifica sobre tráfico alto.
        
        Args:
            current_mb: Tráfico actual en MB/s
            threshold_mb: Umbral configurado en MB/s
        """
        title = "⚠️ High Traffic Alert"
        message = f"Current traffic: {current_mb:.2f} MB/s\nThreshold: {threshold_mb:.2f} MB/s"
        
        return self.notify(title, message, notification_type="high_traffic")
    
    def reset_cooldown(self, notification_type: str = None):
        """
        Reinicia el cooldown para un tipo de notificación específico o todos.
        
        Args:
            notification_type: Tipo específico o None para resetear todos
        """
        if notification_type:
            self.last_notification_time.pop(notification_type, None)
        else:
            self.last_notification_time.clear()
