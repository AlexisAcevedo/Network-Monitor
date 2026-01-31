"""
Tests para las estadísticas de tráfico en DataManager
"""

import pytest
from core.data_manager import DataManager


class TestStatsInitialization:
    """Tests de inicialización de estadísticas"""
    
    def test_init_creates_stats_attributes(self):
        """Verifica que __init__ crea todos los atributos de estadísticas."""
        dm = DataManager()
        
        assert hasattr(dm, "peak_download")
        assert hasattr(dm, "peak_upload")
        assert hasattr(dm, "total_download")
        assert hasattr(dm, "total_upload")
        assert hasattr(dm, "sample_count")
    
    def test_init_stats_start_at_zero(self):
        """Verifica que las estadísticas inician en cero."""
        dm = DataManager()
        
        assert dm.peak_download == 0.0
        assert dm.peak_upload == 0.0
        assert dm.total_download == 0.0
        assert dm.total_upload == 0.0
        assert dm.sample_count == 0


class TestUpdateTrafficStats:
    """Tests de actualización de estadísticas"""
    
    def test_update_traffic_increments_sample_count(self):
        """Verifica que update_traffic incrementa el contador de muestras."""
        dm = DataManager()
        
        dm.update_traffic(10.0, 5.0)
        assert dm.sample_count == 1
        
        dm.update_traffic(15.0, 8.0)
        assert dm.sample_count == 2
    
    def test_update_traffic_updates_peak(self):
        """Verifica que update_traffic actualiza los picos correctamente."""
        dm = DataManager()
        
        dm.update_traffic(10.0, 5.0)
        assert dm.peak_download == 10.0
        assert dm.peak_upload == 5.0
        
        dm.update_traffic(15.0, 3.0)
        assert dm.peak_download == 15.0
        assert dm.peak_upload == 5.0  # No cambia porque 3.0 < 5.0
        
        dm.update_traffic(12.0, 8.0)
        assert dm.peak_download == 15.0  # No cambia
        assert dm.peak_upload == 8.0  # Actualiza porque 8.0 > 5.0
    
    def test_update_traffic_accumulates_total(self):
        """Verifica que update_traffic acumula el total correctamente."""
        dm = DataManager()
        
        dm.update_traffic(10.0, 5.0)
        assert dm.total_download == 10.0
        assert dm.total_upload == 5.0
        
        dm.update_traffic(15.0, 8.0)
        assert dm.total_download == 25.0
        assert dm.total_upload == 13.0
        
        dm.update_traffic(5.0, 2.0)
        assert dm.total_download == 30.0
        assert dm.total_upload == 15.0


class TestGetStats:
    """Tests del método get_stats"""
    
    def test_get_stats_returns_dict(self):
        """Verifica que get_stats retorna un diccionario."""
        dm = DataManager()
        stats = dm.get_stats()
        
        assert isinstance(stats, dict)
    
    def test_get_stats_contains_all_keys(self):
        """Verifica que get_stats contiene todas las claves esperadas."""
        dm = DataManager()
        stats = dm.get_stats()
        
        assert "peak_download" in stats
        assert "peak_upload" in stats
        assert "total_download" in stats
        assert "total_upload" in stats
        assert "avg_download" in stats
        assert "avg_upload" in stats
    
    def test_get_stats_calculates_average(self):
        """Verifica que get_stats calcula el promedio correctamente."""
        dm = DataManager()
        
        dm.update_traffic(10.0, 5.0)
        dm.update_traffic(20.0, 15.0)
        dm.update_traffic(30.0, 10.0)
        
        stats = dm.get_stats()
        
        # Promedio download: (10 + 20 + 30) / 3 = 20.0
        assert stats["avg_download"] == 20.0
        # Promedio upload: (5 + 15 + 10) / 3 = 10.0
        assert stats["avg_upload"] == 10.0
    
    def test_get_stats_average_zero_when_no_samples(self):
        """Verifica que el promedio es 0 cuando no hay muestras."""
        dm = DataManager()
        stats = dm.get_stats()
        
        assert stats["avg_download"] == 0.0
        assert stats["avg_upload"] == 0.0


class TestResetStats:
    """Tests del método reset_stats"""
    
    def test_reset_stats_clears_all_values(self):
        """Verifica que reset_stats reinicia todos los valores a cero."""
        dm = DataManager()
        
        # Generar datos
        dm.update_traffic(10.0, 5.0)
        dm.update_traffic(20.0, 15.0)
        dm.update_traffic(30.0, 10.0)
        
        # Verificar que hay datos
        assert dm.peak_download > 0
        assert dm.total_download > 0
        assert dm.sample_count > 0
        
        # Resetear
        dm.reset_stats()
        
        # Verificar que todo está en cero
        assert dm.peak_download == 0.0
        assert dm.peak_upload == 0.0
        assert dm.total_download == 0.0
        assert dm.total_upload == 0.0
        assert dm.sample_count == 0
    
    def test_reset_stats_allows_new_tracking(self):
        """Verifica que después de reset se puede seguir trackeando."""
        dm = DataManager()
        
        dm.update_traffic(10.0, 5.0)
        dm.reset_stats()
        dm.update_traffic(15.0, 8.0)
        
        stats = dm.get_stats()
        assert stats["peak_download"] == 15.0
        assert stats["total_download"] == 15.0
        assert stats["avg_download"] == 15.0
        assert dm.sample_count == 1
