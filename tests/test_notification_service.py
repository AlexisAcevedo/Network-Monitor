"""
Tests para el servicio de notificaciones (winotify).
"""

import pytest
import time
from core.notification_service import NotificationService


class TestNotificationServiceInit:
    """Tests de inicialización"""
    
    def test_init_creates_cooldown_dict(self):
        """Verifica que __init__ crea el diccionario de cooldown."""
        service = NotificationService()
        assert hasattr(service, "last_notification_time")
        assert isinstance(service.last_notification_time, dict)
        assert len(service.last_notification_time) == 0
    
    def test_init_sets_cooldown_seconds(self):
        """Verifica que el cooldown es 30 segundos."""
        service = NotificationService()
        assert service.cooldown_seconds == 30


class TestNotify:
    """Tests del método notify"""
    
    def test_notify_returns_boolean(self, mocker):
        """Verifica que notify retorna un booleano."""
        service = NotificationService()
        mock_notification = mocker.patch("core.notification_service.Notification")
        
        result = service.notify("Test", "Message")
        assert isinstance(result, bool)
    
    def test_notify_calls_show(self, mocker):
        """Verifica que notify llama a show."""
        service = NotificationService()
        mock_notification_class = mocker.patch("core.notification_service.Notification")
        mock_instance = mock_notification_class.return_value
        
        service.notify("Test Title", "Test Message")
        
        mock_notification_class.assert_called_once()
        mock_instance.show.assert_called_once()
    
    def test_notify_respects_cooldown(self, mocker):
        """Verifica que notify respeta el cooldown."""
        service = NotificationService()
        mock_notification = mocker.patch("core.notification_service.Notification")
        
        # Primera notificación debe funcionar
        result1 = service.notify("Test", "Message", notification_type="test")
        assert result1 is True
        
        # Segunda notificación inmediata debe ser bloqueada
        result2 = service.notify("Test", "Message", notification_type="test")
        assert result2 is False
        
        # Solo debe haberse llamado una vez
        assert mock_notification.call_count == 1
    
    def test_notify_different_types_no_cooldown(self, mocker):
        """Verifica que diferentes tipos de notificación no comparten cooldown."""
        service = NotificationService()
        mock_notification = mocker.patch("core.notification_service.Notification")
        
        # Dos notificaciones de diferentes tipos
        result1 = service.notify("Test1", "Message1", notification_type="type1")
        result2 = service.notify("Test2", "Message2", notification_type="type2")
        
        assert result1 is True
        assert result2 is True
        assert mock_notification.call_count == 2


class TestNotifyNewDevice:
    """Tests del método notify_new_device"""
    
    def test_notify_new_device_formats_message(self, mocker):
        """Verifica que notify_new_device formatea el mensaje correctamente."""
        service = NotificationService()
        mock_notify = mocker.patch.object(service, "notify", return_value=True)
        
        device = {
            "ip": "192.168.1.100",
            "mac": "AA:BB:CC:DD:EE:FF",
            "vendor": "Apple Inc."
        }
        
        service.notify_new_device(device)
        
        mock_notify.assert_called_once()
        call_args = mock_notify.call_args
        
        assert "New Device Detected" in call_args[0][0]
        assert "192.168.1.100" in call_args[0][1]
        assert "Apple Inc." in call_args[0][1]
    
    def test_notify_new_device_handles_missing_fields(self, mocker):
        """Verifica que maneja campos faltantes con 'Unknown'."""
        service = NotificationService()
        mock_notify = mocker.patch.object(service, "notify", return_value=True)
        
        device = {"ip": "192.168.1.100"}  # Solo IP
        
        service.notify_new_device(device)
        
        call_args = mock_notify.call_args
        assert "Unknown" in call_args[0][1]


class TestNotifyHighTraffic:
    """Tests del método notify_high_traffic"""
    
    def test_notify_high_traffic_formats_message(self, mocker):
        """Verifica que notify_high_traffic formatea el mensaje correctamente."""
        service = NotificationService()
        mock_notify = mocker.patch.object(service, "notify", return_value=True)
        
        service.notify_high_traffic(75.5, 50.0)
        
        mock_notify.assert_called_once()
        call_args = mock_notify.call_args
        
        assert "High Traffic" in call_args[0][0]
        assert "75.50" in call_args[0][1]
        assert "50.00" in call_args[0][1]


class TestResetCooldown:
    """Tests del método reset_cooldown"""
    
    def test_reset_cooldown_specific_type(self, mocker):
        """Verifica que reset_cooldown elimina un tipo específico."""
        service = NotificationService()
        mock_notification = mocker.patch("core.notification_service.Notification")
        
        # Generar cooldown
        service.notify("Test", "Message", notification_type="type1")
        service.notify("Test", "Message", notification_type="type2")
        
        assert "type1" in service.last_notification_time
        assert "type2" in service.last_notification_time
        
        # Resetear solo type1
        service.reset_cooldown("type1")
        
        assert "type1" not in service.last_notification_time
        assert "type2" in service.last_notification_time
    
    def test_reset_cooldown_all(self, mocker):
        """Verifica que reset_cooldown sin argumentos limpia todo."""
        service = NotificationService()
        mock_notification = mocker.patch("core.notification_service.Notification")
        
        # Generar cooldowns
        service.notify("Test", "Message", notification_type="type1")
        service.notify("Test", "Message", notification_type="type2")
        
        assert len(service.last_notification_time) == 2
        
        # Resetear todo
        service.reset_cooldown()
        
        assert len(service.last_notification_time) == 0
