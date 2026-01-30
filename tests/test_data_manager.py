"""
Tests unitarios para DataManager (core/data_manager.py).
Cubre gestión de buffer circular, actualización de datos y escala dinámica.
"""

import pytest
from unittest.mock import Mock, patch
from collections import deque
from core.data_manager import DataManager


class TestDataManagerInit:
    """Tests de inicialización de DataManager."""
    
    @patch("flet_charts.LineChartDataPoint")
    def test_init_creates_60_download_points(self, mock_point):
        """Crea exactamente 60 puntos para download."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        
        # Act
        manager = DataManager()
        
        # Assert
        assert len(manager.download_points) == 60
        assert mock_point.call_count >= 60
    
    @patch("flet_charts.LineChartDataPoint")
    def test_init_creates_60_upload_points(self, mock_point):
        """Crea exactamente 60 puntos para upload."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        
        # Act
        manager = DataManager()
        
        # Assert
        assert len(manager.upload_points) == 60
    
    @patch("flet_charts.LineChartDataPoint")
    def test_init_creates_deques_with_maxlen_60(self, mock_point):
        """Crea deques con maxlen=60."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        
        # Act
        manager = DataManager()
        
        # Assert
        assert isinstance(manager.download_values, deque)
        assert isinstance(manager.upload_values, deque)
        assert manager.download_values.maxlen == 60
        assert manager.upload_values.maxlen == 60
    
    @patch("flet_charts.LineChartDataPoint")
    def test_init_deques_filled_with_zeros(self, mock_point):
        """Deques inicializados con 60 ceros."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        
        # Act
        manager = DataManager()
        
        # Assert
        assert len(manager.download_values) == 60
        assert len(manager.upload_values) == 60
        assert all(v == 0 for v in manager.download_values)
        assert all(v == 0 for v in manager.upload_values)


class TestUpdateTraffic:
    """Tests del método update_traffic."""
    
    @patch("flet_charts.LineChartDataPoint")
    def test_update_traffic_appends_values(self, mock_point):
        """Agrega nuevos valores a los deques."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        manager.update_traffic(5.5, 3.2)
        
        # Assert
        assert manager.download_values[-1] == 5.5
        assert manager.upload_values[-1] == 3.2
    
    @patch("flet_charts.LineChartDataPoint")
    def test_update_traffic_updates_points(self, mock_point):
        """Actualiza los valores y de los puntos gráficos."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        manager.update_traffic(10.0, 5.0)
        
        # Assert
        # El último punto debe tener el nuevo valor
        assert manager.download_points[-1].y == 10.0
        assert manager.upload_points[-1].y == 5.0
    
    @patch("flet_charts.LineChartDataPoint")
    def test_update_traffic_multiple_updates(self, mock_point):
        """Múltiples actualizaciones funcionan correctamente."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        manager.update_traffic(1.0, 0.5)
        manager.update_traffic(2.0, 1.0)
        manager.update_traffic(3.0, 1.5)
        
        # Assert
        assert manager.download_values[-1] == 3.0
        assert manager.upload_values[-1] == 1.5
        assert manager.download_values[-2] == 2.0
        assert manager.upload_values[-2] == 1.0
    
    @patch("flet_charts.LineChartDataPoint")
    def test_update_traffic_syncs_deque_and_points(self, mock_point):
        """Los valores en deque y puntos están sincronizados."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        manager.update_traffic(7.5, 4.2)
        
        # Assert
        for point, value in zip(manager.download_points, manager.download_values):
            assert point.y == value
        for point, value in zip(manager.upload_points, manager.upload_values):
            assert point.y == value


class TestCalculateDynamicScale:
    """Tests del método calculate_dynamic_scale."""
    
    @patch("flet_charts.LineChartDataPoint")
    def test_calculate_scale_minimum_100(self, mock_point):
        """Retorna mínimo 100 para valores bajos."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        result = manager.calculate_dynamic_scale(5.0, 3.0)
        
        # Assert
        assert result == 100
    
    @patch("flet_charts.LineChartDataPoint")
    def test_calculate_scale_zero_traffic(self, mock_point):
        """Retorna 100 para tráfico cero."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        result = manager.calculate_dynamic_scale(0.0, 0.0)
        
        # Assert
        assert result == 100
    
    @patch("flet_charts.LineChartDataPoint")
    def test_calculate_scale_growth_blocks_of_5(self, mock_point):
        """Crece en bloques de 5 MB sobre 100."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        manager.update_traffic(102.0, 50.0)
        
        # Act
        result = manager.calculate_dynamic_scale(102.0, 50.0)
        
        # Assert
        # max_val = 102, ceil(102/5) = 21, 21*5 = 105, +5 = 110
        assert result == 110
    
    @patch("flet_charts.LineChartDataPoint")
    def test_calculate_scale_uses_historical_max(self, mock_point):
        """Usa el máximo histórico, no solo el valor actual."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Agregamos un pico alto
        manager.update_traffic(150.0, 50.0)
        
        # Act
        # Ahora el tráfico baja, pero la escala debe considerar el pico
        result = manager.calculate_dynamic_scale(10.0, 5.0)
        
        # Assert
        # max_val = 150, ceil(150/5) = 30, 30*5 = 150, +5 = 155
        assert result == 155
    
    @patch("flet_charts.LineChartDataPoint")
    def test_calculate_scale_exact_multiple_of_5(self, mock_point):
        """Maneja correctamente múltiplos exactos de 5."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        manager.update_traffic(105.0, 50.0)
        
        # Act
        result = manager.calculate_dynamic_scale(105.0, 50.0)
        
        # Assert
        # max_val = 105, ceil(105/5) = 21, 21*5 = 105, +5 = 110
        assert result == 110


class TestDequeMaxlen:
    """Tests del comportamiento del buffer circular (deque maxlen)."""
    
    @patch("flet_charts.LineChartDataPoint")
    def test_deque_maxlen_overflow(self, mock_point):
        """Deque descarta valores antiguos al superar maxlen."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        # Agregamos 61 valores (uno más que maxlen=60)
        for i in range(61):
            manager.update_traffic(float(i), float(i))
        
        # Assert
        assert len(manager.download_values) == 60
        assert manager.download_values[0] == 1.0  # El primer 0 fue descartado
        assert manager.download_values[-1] == 60.0
    
    @patch("flet_charts.LineChartDataPoint")
    def test_deque_maintains_order(self, mock_point):
        """Deque mantiene el orden FIFO."""
        # Arrange
        mock_point.side_effect = lambda x, y: Mock(x=x, y=y)
        manager = DataManager()
        
        # Act
        for i in range(10):
            manager.update_traffic(float(i), float(i * 2))
        
        # Assert
        # Los últimos 10 valores deben ser 0-9
        assert list(manager.download_values)[-10:] == [float(i) for i in range(10)]
        assert list(manager.upload_values)[-10:] == [float(i * 2) for i in range(10)]
