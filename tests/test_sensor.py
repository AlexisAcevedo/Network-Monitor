"""
Tests unitarios para NetworkSensor (core/sensor.py).
Cubre monitoreo de tráfico y formateo de bytes.
"""

import pytest
from unittest.mock import Mock, patch
from collections import namedtuple
from core.sensor import NetworkSensor


# Helper: Crear namedtuple compatible con psutil
NetIOCounters = namedtuple(
    "NetIOCounters",
    ["bytes_sent", "bytes_recv", "packets_sent", "packets_recv", 
     "errin", "errout", "dropin", "dropout"]
)


class TestNetworkSensorInit:
    """Tests de inicialización de NetworkSensor."""
    
    def test_init_stores_initial_counters(self, mocker):
        """Verifica que __init__ almacena los contadores iniciales."""
        # Arrange
        initial_counters = NetIOCounters(
            bytes_sent=1000,
            bytes_recv=2000,
            packets_sent=10,
            packets_recv=20,
            errin=0, errout=0, dropin=0, dropout=0
        )
        mocker.patch("psutil.net_io_counters", return_value=initial_counters)
        
        # Act
        sensor = NetworkSensor()
        
        # Assert
        assert sensor.io_prev == initial_counters
        assert sensor.io_prev.bytes_sent == 1000
        assert sensor.io_prev.bytes_recv == 2000


class TestGetTraffic:
    """Tests del método get_traffic."""
    
    def test_get_traffic_calculates_delta(self, mocker):
        """Calcula correctamente el diferencial de tráfico."""
        # Arrange
        initial = NetIOCounters(
            bytes_sent=1000, bytes_recv=2000,
            packets_sent=10, packets_recv=20,
            errin=0, errout=0, dropin=0, dropout=0
        )
        current = NetIOCounters(
            bytes_sent=2000, bytes_recv=4000,
            packets_sent=20, packets_recv=40,
            errin=0, errout=0, dropin=0, dropout=0
        )
        
        mock_counters = mocker.patch("psutil.net_io_counters")
        mock_counters.side_effect = [initial, current]
        
        sensor = NetworkSensor()
        
        # Act
        download_mb, upload_mb = sensor.get_traffic()
        
        # Assert
        # Delta: upload = 2000 - 1000 = 1000 bytes = 0.000954 MB
        # Delta: download = 4000 - 2000 = 2000 bytes = 0.001907 MB
        assert upload_mb == pytest.approx(1000 / 1048576, rel=1e-5)
        assert download_mb == pytest.approx(2000 / 1048576, rel=1e-5)
    
    def test_get_traffic_returns_mb(self, mocker):
        """Retorna valores en megabytes."""
        # Arrange
        initial = NetIOCounters(
            bytes_sent=0, bytes_recv=0,
            packets_sent=0, packets_recv=0,
            errin=0, errout=0, dropin=0, dropout=0
        )
        # 1 MB = 1048576 bytes
        current = NetIOCounters(
            bytes_sent=1048576, bytes_recv=2097152,  # 1 MB sent, 2 MB recv
            packets_sent=100, packets_recv=200,
            errin=0, errout=0, dropin=0, dropout=0
        )
        
        mock_counters = mocker.patch("psutil.net_io_counters")
        mock_counters.side_effect = [initial, current]
        
        sensor = NetworkSensor()
        
        # Act
        download_mb, upload_mb = sensor.get_traffic()
        
        # Assert
        assert upload_mb == pytest.approx(1.0, rel=1e-5)
        assert download_mb == pytest.approx(2.0, rel=1e-5)
    
    def test_get_traffic_updates_reference(self, mocker):
        """Actualiza la referencia io_prev después de cada lectura."""
        # Arrange
        counter1 = NetIOCounters(
            bytes_sent=1000, bytes_recv=2000,
            packets_sent=10, packets_recv=20,
            errin=0, errout=0, dropin=0, dropout=0
        )
        counter2 = NetIOCounters(
            bytes_sent=2000, bytes_recv=4000,
            packets_sent=20, packets_recv=40,
            errin=0, errout=0, dropin=0, dropout=0
        )
        counter3 = NetIOCounters(
            bytes_sent=3000, bytes_recv=6000,
            packets_sent=30, packets_recv=60,
            errin=0, errout=0, dropin=0, dropout=0
        )
        
        mock_counters = mocker.patch("psutil.net_io_counters")
        mock_counters.side_effect = [counter1, counter2, counter3]
        
        sensor = NetworkSensor()
        
        # Act
        sensor.get_traffic()  # Primera lectura
        download_mb, upload_mb = sensor.get_traffic()  # Segunda lectura
        
        # Assert
        # Segunda lectura debe calcular delta desde counter2, no counter1
        assert sensor.io_prev == counter3
        assert upload_mb == pytest.approx(1000 / 1048576, rel=1e-5)
        assert download_mb == pytest.approx(2000 / 1048576, rel=1e-5)
    
    def test_get_traffic_zero_delta(self, mocker):
        """Maneja correctamente delta cero (sin tráfico)."""
        # Arrange
        same_counter = NetIOCounters(
            bytes_sent=1000, bytes_recv=2000,
            packets_sent=10, packets_recv=20,
            errin=0, errout=0, dropin=0, dropout=0
        )
        
        mock_counters = mocker.patch("psutil.net_io_counters")
        mock_counters.return_value = same_counter
        
        sensor = NetworkSensor()
        
        # Act
        download_mb, upload_mb = sensor.get_traffic()
        
        # Assert
        assert upload_mb == 0.0
        assert download_mb == 0.0


class TestFormatBytes:
    """Tests del método format_bytes."""
    
    def test_format_bytes_zero(self):
        """Formatea correctamente 0 bytes."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(0)
        
        # Assert
        assert result == "0.00 B"
    
    def test_format_bytes_bytes_unit(self):
        """Formatea valores menores a 1 KB."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(512)
        
        # Assert
        assert result == "512.00 B"
    
    def test_format_bytes_kilobytes(self):
        """Formatea correctamente kilobytes."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1024)
        
        # Assert
        assert result == "1.00 KB"
    
    def test_format_bytes_megabytes(self):
        """Formatea correctamente megabytes."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1048576)  # 1 MB
        
        # Assert
        assert result == "1.00 MB"
    
    def test_format_bytes_gigabytes(self):
        """Formatea correctamente gigabytes."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1073741824)  # 1 GB
        
        # Assert
        assert result == "1.00 GB"
    
    def test_format_bytes_terabytes(self):
        """Formatea correctamente terabytes."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1099511627776)  # 1 TB
        
        # Assert
        assert result == "1.00 TB"
    
    def test_format_bytes_petabytes(self):
        """Formatea valores mayores a 1 PB."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1125899906842624)  # 1 PB
        
        # Assert
        assert result == "1.00 PB"
    
    def test_format_bytes_decimal_precision(self):
        """Mantiene 2 decimales de precisión."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(1536)  # 1.5 KB
        
        # Assert
        assert result == "1.50 KB"
    
    def test_format_bytes_large_value(self):
        """Maneja valores muy grandes correctamente."""
        # Arrange
        sensor = NetworkSensor()
        
        # Act
        result = sensor.format_bytes(5368709120)  # ~5 GB
        
        # Assert
        assert "5.00 GB" in result
