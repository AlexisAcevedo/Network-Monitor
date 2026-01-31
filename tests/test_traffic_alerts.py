"""
Tests adicionales para alertas de tráfico alto en DataManager
"""

import pytest
from core.data_manager import DataManager


class TestTrafficThreshold:
    """Tests de configuración de umbral"""
    
    def test_init_sets_default_threshold(self):
        """Verifica que el umbral por defecto es 10 MB/s."""
        dm = DataManager()
        assert dm.traffic_threshold_mb == 10.0
    
    def test_init_alerts_disabled_by_default(self):
        """Verifica que las alertas están deshabilitadas por defecto."""
        dm = DataManager()
        assert dm.high_traffic_alerts_enabled is False
    
    def test_set_traffic_threshold(self):
        """Verifica que set_traffic_threshold actualiza el umbral."""
        dm = DataManager()
        
        dm.set_traffic_threshold(25.5)
        assert dm.traffic_threshold_mb == 25.5
    
    def test_set_traffic_threshold_minimum(self):
        """Verifica que el umbral mínimo es 0.1 MB/s."""
        dm = DataManager()
        
        dm.set_traffic_threshold(0.05)
        assert dm.traffic_threshold_mb == 0.1
        
        dm.set_traffic_threshold(-5.0)
        assert dm.traffic_threshold_mb == 0.1


class TestCheckHighTraffic:
    """Tests de verificación de tráfico alto"""
    
    def test_check_high_traffic_disabled_returns_false(self):
        """Verifica que retorna False cuando las alertas están deshabilitadas."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = False
        
        result = dm.check_high_traffic(50.0, 5.0)
        assert result is False
    
    def test_check_high_traffic_below_threshold(self):
        """Verifica que retorna False cuando el tráfico está bajo el umbral."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = True
        
        result = dm.check_high_traffic(5.0, 3.0)
        assert result is False
    
    def test_check_high_traffic_download_exceeds(self):
        """Verifica que retorna True cuando download supera el umbral."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = True
        
        result = dm.check_high_traffic(15.0, 3.0)
        assert result is True
    
    def test_check_high_traffic_upload_exceeds(self):
        """Verifica que retorna True cuando upload supera el umbral."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = True
        
        result = dm.check_high_traffic(5.0, 12.0)
        assert result is True
    
    def test_check_high_traffic_both_exceed(self):
        """Verifica que retorna True cuando ambos superan el umbral."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = True
        
        result = dm.check_high_traffic(15.0, 20.0)
        assert result is True
    
    def test_check_high_traffic_exactly_at_threshold(self):
        """Verifica que retorna False cuando el tráfico es exactamente el umbral."""
        dm = DataManager()
        dm.set_traffic_threshold(10.0)
        dm.high_traffic_alerts_enabled = True
        
        result = dm.check_high_traffic(10.0, 10.0)
        assert result is False
