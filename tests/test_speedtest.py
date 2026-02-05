"""
Tests unitarios para SpeedtestService (core/speedtest_service.py).
Cubre ejecución de tests, manejo de errores y obtención de servidores.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestSpeedtestServiceInit:
    """Tests de inicialización de SpeedtestService."""
    
    def test_init_creates_instance(self):
        """Verifica que se puede crear una instancia."""
        from core.speedtest_service import SpeedtestService
        
        service = SpeedtestService()
        
        assert service is not None
        assert service._speedtest is None
        assert service._last_result is None


class TestRunTest:
    """Tests del método run_test."""
    
    def test_run_test_returns_dict(self, mocker):
        """Verifica que run_test retorna un diccionario."""
        from core.speedtest_service import SpeedtestService
        
        # Mock speedtest.Speedtest
        mock_speedtest = MagicMock()
        mock_speedtest.results.server = {"sponsor": "Test ISP", "name": "Test City"}
        mock_speedtest.results.ping = 15.5
        mock_speedtest.download.return_value = 100_000_000  # 100 Mbps
        mock_speedtest.upload.return_value = 50_000_000     # 50 Mbps
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        result = service.run_test()
        
        assert isinstance(result, dict)
        assert "download_mbps" in result
        assert "upload_mbps" in result
        assert "ping_ms" in result
        assert "server_name" in result
        assert "error" in result
    
    def test_run_test_calculates_mbps_correctly(self, mocker):
        """Verifica conversión correcta de bps a Mbps."""
        from core.speedtest_service import SpeedtestService
        
        mock_speedtest = MagicMock()
        mock_speedtest.results.server = {"sponsor": "ISP", "name": "City"}
        mock_speedtest.results.ping = 20.0
        mock_speedtest.download.return_value = 100_000_000  # 100 Mbps
        mock_speedtest.upload.return_value = 25_000_000     # 25 Mbps
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        result = service.run_test()
        
        assert result["download_mbps"] == 100.0
        assert result["upload_mbps"] == 25.0
        assert result["ping_ms"] == 20.0
        assert result["error"] is False
    
    def test_run_test_handles_exception(self, mocker):
        """Verifica manejo de errores de conexión."""
        from core.speedtest_service import SpeedtestService
        
        mock_speedtest = MagicMock()
        mock_speedtest.get_best_server.side_effect = Exception("Network error")
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        result = service.run_test()
        
        assert result["error"] is True
        assert result["download_mbps"] == 0
        assert result["upload_mbps"] == 0
        assert "error_message" in result
    
    def test_run_test_stores_last_result(self, mocker):
        """Verifica que guarda el último resultado."""
        from core.speedtest_service import SpeedtestService
        
        mock_speedtest = MagicMock()
        mock_speedtest.results.server = {"sponsor": "ISP", "name": "City"}
        mock_speedtest.results.ping = 10.0
        mock_speedtest.download.return_value = 50_000_000
        mock_speedtest.upload.return_value = 10_000_000
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        service.run_test()
        
        last = service.get_last_result()
        assert last is not None
        assert last["download_mbps"] == 50.0


class TestGetServers:
    """Tests del método get_servers."""
    
    def test_get_servers_returns_list(self, mocker):
        """Verifica que get_servers retorna una lista."""
        from core.speedtest_service import SpeedtestService
        
        mock_speedtest = MagicMock()
        mock_speedtest.servers = {
            1: [{"id": "1", "name": "Server1", "sponsor": "ISP1", "country": "AR", "latency": 10}],
            2: [{"id": "2", "name": "Server2", "sponsor": "ISP2", "country": "AR", "latency": 20}]
        }
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        servers = service.get_servers()
        
        assert isinstance(servers, list)
    
    def test_get_servers_handles_exception(self, mocker):
        """Verifica manejo de errores al obtener servidores."""
        from core.speedtest_service import SpeedtestService
        
        mock_speedtest = MagicMock()
        mock_speedtest.get_servers.side_effect = Exception("Error")
        mocker.patch("core.speedtest_service.speedtest.Speedtest", return_value=mock_speedtest)
        
        service = SpeedtestService()
        servers = service.get_servers()
        
        assert servers == []


class TestGetLastResult:
    """Tests del método get_last_result."""
    
    def test_get_last_result_initially_none(self):
        """Verifica que inicialmente es None."""
        from core.speedtest_service import SpeedtestService
        
        service = SpeedtestService()
        
        assert service.get_last_result() is None
