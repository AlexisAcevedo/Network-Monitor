"""
Tests unitarios para NetworkScanner (core/scanner.py).
Cubre detección de IP local, escaneo de red y manejo de errores.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.scanner import NetworkScanner


class TestNetworkScannerInit:
    """Tests de inicialización de NetworkScanner."""
    
    def test_init_creates_target_ip(self, mock_socket):
        """Verifica que __init__ crea el atributo target_ip."""
        # Arrange & Act
        scanner = NetworkScanner()
        
        # Assert
        assert hasattr(scanner, "target_ip")
        assert scanner.target_ip is not None
    
    def test_init_calls_get_local_range(self, mock_socket):
        """Verifica que __init__ llama a get_local_range."""
        # Arrange & Act
        with patch.object(NetworkScanner, "get_local_range", return_value="192.168.1.1/24") as mock_method:
            scanner = NetworkScanner()
        
        # Assert
        mock_method.assert_called_once()


class TestGetLocalRange:
    """Tests del método get_local_range."""
    
    def test_get_local_range_success(self, mocker):
        """Detecta IP local correctamente y genera rango /24."""
        # Arrange
        mock_sock = MagicMock()
        mock_sock.getsockname.return_value = ("192.168.100.45", 12345)
        mocker.patch("socket.socket", return_value=mock_sock)
        
        scanner = NetworkScanner()
        
        # Act
        result = scanner.target_ip
        
        # Assert
        assert result == "192.168.100.1/24"
        mock_sock.connect.assert_called_once_with(("8.8.8.8", 80))
        mock_sock.close.assert_called_once()
    
    def test_get_local_range_different_subnet(self, mocker):
        """Funciona con diferentes subredes."""
        # Arrange
        mock_sock = MagicMock()
        mock_sock.getsockname.return_value = ("10.0.5.123", 12345)
        mocker.patch("socket.socket", return_value=mock_sock)
        
        scanner = NetworkScanner()
        
        # Act
        result = scanner.target_ip
        
        # Assert
        assert result == "10.0.5.1/24"
    
    def test_get_local_range_fallback_on_exception(self, mocker):
        """Retorna fallback cuando falla la detección."""
        # Arrange
        mock_sock = MagicMock()
        mock_sock.connect.side_effect = Exception("Network error")
        mocker.patch("socket.socket", return_value=mock_sock)
        
        scanner = NetworkScanner()
        
        # Act
        result = scanner.target_ip
        
        # Assert
        assert result == "192.168.1.1/24"  # Fallback


class TestScanNetwork:
    """Tests del método scan_network."""
    
    def test_scan_network_returns_list(self, mocker, mock_socket):
        """Retorna una lista (vacía o con dispositivos)."""
        # Arrange
        mocker.patch("scapy.all.srp", return_value=([], []))
        scanner = NetworkScanner()
        
        # Act
        result = scanner.scan_network()
        
        # Assert
        assert isinstance(result, list)
    
    def test_scan_network_success_with_devices(self, mocker, mock_socket):
        """Escaneo exitoso retorna lista de dispositivos."""
        # Arrange
        # Mock de respuesta ARP
        mock_response = Mock()
        mock_response.psrc = "192.168.1.10"
        mock_response.hwsrc = "aa:bb:cc:dd:ee:ff"
        
        answered = [(Mock(), mock_response)]
        mocker.patch("scapy.all.srp", return_value=(answered, []))
        
        scanner = NetworkScanner()
        
        # Act
        result = scanner.scan_network()
        
        # Assert
        assert len(result) == 1
        assert result[0]["ip"] == "192.168.1.10"
        assert result[0]["mac"] == "aa:bb:cc:dd:ee:ff"
    
    def test_scan_network_multiple_devices(self, mocker, mock_socket):
        """Detecta múltiples dispositivos correctamente."""
        # Arrange
        mock_resp1 = Mock()
        mock_resp1.psrc = "192.168.1.1"
        mock_resp1.hwsrc = "11:22:33:44:55:66"
        
        mock_resp2 = Mock()
        mock_resp2.psrc = "192.168.1.2"
        mock_resp2.hwsrc = "aa:bb:cc:dd:ee:ff"
        
        answered = [(Mock(), mock_resp1), (Mock(), mock_resp2)]
        mocker.patch("scapy.all.srp", return_value=(answered, []))
        
        scanner = NetworkScanner()
        
        # Act
        result = scanner.scan_network()
        
        # Assert
        assert len(result) == 2
        assert result[0]["ip"] == "192.168.1.1"
        assert result[1]["ip"] == "192.168.1.2"
    
    def test_scan_network_empty_network(self, mocker, mock_socket):
        """Red sin dispositivos retorna lista vacía."""
        # Arrange
        mocker.patch("scapy.all.srp", return_value=([], []))
        scanner = NetworkScanner()
        
        # Act
        result = scanner.scan_network()
        
        # Assert
        assert result == []
    
    def test_scan_network_handles_exception(self, mocker, mock_socket):
        """Maneja excepciones de scapy y retorna lista vacía."""
        # Arrange
        mocker.patch("scapy.all.srp", side_effect=Exception("Scapy error"))
        scanner = NetworkScanner()
        
        # Act
        result = scanner.scan_network()
        
        # Assert
        assert result == []
    
    def test_scan_network_uses_correct_timeout(self, mocker, mock_socket):
        """Verifica que usa timeout de 1 segundo."""
        # Arrange
        mock_srp = mocker.patch("scapy.all.srp", return_value=([], []))
        scanner = NetworkScanner()
        
        # Act
        scanner.scan_network()
        
        # Assert
        # Verificamos que srp fue llamado con timeout=1
        call_kwargs = mock_srp.call_args[1]
        assert call_kwargs["timeout"] == 1
        assert call_kwargs["verbose"] is False
