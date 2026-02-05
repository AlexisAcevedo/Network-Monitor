"""
Tests unitarios para PortScanner (core/port_scanner.py).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.port_scanner import PortScanner, ScanMode
import socket

class TestPortScanner:
    
    def test_init(self):
        """Verifica inicialización."""
        scanner = PortScanner()
        assert isinstance(scanner.TOP_20_PORTS, list)
        assert len(scanner.TOP_20_PORTS) == 20

    def test_get_service_name_known(self):
        """Verifica detección de nombres de servicios conocidos."""
        scanner = PortScanner()
        assert scanner.get_service_name(80) == "http"
        assert scanner.get_service_name(443) == "https"
        
    def test_get_service_name_unknown(self):
        """Verifica fallback para servicios desconocidos."""
        scanner = PortScanner()
        # Mockeamos socket.getservbyport para que lance error
        with patch("socket.getservbyport", side_effect=OSError):
            assert scanner.get_service_name(99999) == "unknown"

    def test_scan_port_open(self, mocker):
        """Verifica detección de puerto abierto."""
        scanner = PortScanner()
        
        # Mock socket
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0 # 0 = Success (Open)
        mock_socket.__enter__.return_value = mock_socket
        
        mocker.patch("socket.socket", return_value=mock_socket)
        
        result = scanner.scan_port("192.168.1.1", 80)
        assert result is not None
        assert result["port"] == 80
        assert result["state"] == "open"

    def test_scan_port_closed(self, mocker):
        """Verifica detección de puerto cerrado."""
        scanner = PortScanner()
        
        # Mock socket
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 111 # != 0 (Error/Closed)
        mock_socket.__enter__.return_value = mock_socket
        
        mocker.patch("socket.socket", return_value=mock_socket)
        
        result = scanner.scan_port("192.168.1.1", 80)
        assert result is None

    def test_scan_mode_quick(self, mocker):
        """Verifica que Quick Mode escanea los puertos correctos."""
        scanner = PortScanner()
        
        # Mock scan_port para evitar red real y contar llamadas
        mock_scan = mocker.patch.object(scanner, "scan_port", return_value=None)
        
        scanner.scan("192.168.1.1", mode=ScanMode.QUICK)
        
        assert mock_scan.call_count == 20

    def test_scan_mode_standard(self, mocker):
        """Verifica que Standard Mode escanea > 20 puertos."""
        scanner = PortScanner()
        mock_scan = mocker.patch.object(scanner, "scan_port", return_value=None)
        
        scanner.scan("192.168.1.1", mode=ScanMode.STANDARD)
        
        assert mock_scan.call_count == len(scanner.TOP_100_PORTS)

    def test_scan_returns_results(self, mocker):
        """Verifica que scan retorna lista de puertos abiertos."""
        scanner = PortScanner()
        
        # Simulamos que el puerto 80 está abierto y el resto cerrados
        def side_effect(ip, port, timeout):
            if port == 80:
                return {"port": 80, "state": "open", "service": "http"}
            return None
            
        mocker.patch.object(scanner, "scan_port", side_effect=side_effect)
        
        results = scanner.scan("192.168.1.1", mode=ScanMode.QUICK)
        
        assert len(results) == 1
        assert results[0]["port"] == 80
