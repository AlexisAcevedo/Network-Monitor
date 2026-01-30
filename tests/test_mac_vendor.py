"""
Tests unitarios para MacVendorService (core/mac_vendor.py).
Cubre consultas de vendor, caché, manejo de errores y timeouts.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from core.mac_vendor import MacVendorService
import requests


class TestMacVendorServiceInit:
    """Tests de inicialización de MacVendorService."""
    
    def test_init_creates_empty_cache(self):
        """Verifica que __init__ crea un caché vacío."""
        # Arrange & Act
        service = MacVendorService()
        
        # Assert
        assert hasattr(service, "cache")
        assert isinstance(service.cache, dict)
        assert len(service.cache) == 0
    
    def test_init_sets_api_url(self):
        """Verifica que __init__ configura la URL de la API."""
        # Arrange & Act
        service = MacVendorService()
        
        # Assert
        assert hasattr(service, "api_url")
        assert service.api_url == "https://api.macvendors.com/"
    
    def test_init_sets_timeout(self):
        """Verifica que __init__ configura el timeout."""
        # Arrange & Act
        service = MacVendorService()
        
        # Assert
        assert hasattr(service, "timeout")
        assert service.timeout == 2


class TestGetVendor:
    """Tests del método get_vendor."""
    
    def test_get_vendor_success(self, mocker):
        """Consulta exitosa retorna nombre del fabricante."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Apple, Inc."
        mocker.patch("requests.get", return_value=mock_response)
        
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("00:1A:2B:3C:4D:5E")
        
        # Assert
        assert result == "Apple, Inc."
    
    def test_get_vendor_normalizes_mac(self, mocker):
        """Normaliza la MAC address a mayúsculas para el caché."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Samsung Electronics"
        mocker.patch("requests.get", return_value=mock_response)
        
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("aa:bb:cc:dd:ee:ff")
        
        # Assert
        assert "AA:BB:CC:DD:EE:FF" in service.cache
        assert result == "Samsung Electronics"
    
    def test_get_vendor_uses_cache(self, mocker):
        """Usa el caché en lugar de hacer consultas repetidas."""
        # Arrange
        mock_get = mocker.patch("requests.get")
        service = MacVendorService()
        
        # Pre-llenar el caché
        service.cache["AA:BB:CC:DD:EE:FF"] = "Cached Vendor"
        
        # Act
        result = service.get_vendor("aa:bb:cc:dd:ee:ff")
        
        # Assert
        assert result == "Cached Vendor"
        mock_get.assert_not_called()  # No debe hacer consulta HTTP
    
    def test_get_vendor_invalid_mac_format(self):
        """Retorna 'Unknown' para formato de MAC inválido."""
        # Arrange
        service = MacVendorService()
        
        # Act & Assert
        assert service.get_vendor("") == "Unknown"
        assert service.get_vendor("123") == "Unknown"
        assert service.get_vendor(None) == "Unknown"
    
    def test_get_vendor_not_found_404(self, mocker):
        """Retorna 'Unknown' cuando la API retorna 404."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mocker.patch("requests.get", return_value=mock_response)
        
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("FF:FF:FF:FF:FF:FF")
        
        # Assert
        assert result == "Unknown"
    
    def test_get_vendor_caches_unknown(self, mocker):
        """Cachea 'Unknown' para evitar consultas repetidas."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mocker.patch("requests.get", return_value=mock_response)
        
        service = MacVendorService()
        
        # Act
        service.get_vendor("FF:FF:FF:FF:FF:FF")
        
        # Assert
        assert service.cache["FF:FF:FF:FF:FF:FF"] == "Unknown"
    
    def test_get_vendor_timeout(self, mocker):
        """Maneja timeout de forma elegante."""
        # Arrange
        mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("00:11:22:33:44:55")
        
        # Assert
        assert result == "Unknown"
    
    def test_get_vendor_network_error(self, mocker):
        """Maneja errores de red de forma elegante."""
        # Arrange
        mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Network error"))
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("00:11:22:33:44:55")
        
        # Assert
        assert result == "Unknown"
    
    def test_get_vendor_unexpected_error(self, mocker):
        """Maneja errores inesperados de forma elegante."""
        # Arrange
        mocker.patch("requests.get", side_effect=Exception("Unexpected error"))
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("00:11:22:33:44:55")
        
        # Assert
        assert result == "Unknown"
    
    def test_get_vendor_uses_correct_timeout(self, mocker):
        """Verifica que usa el timeout configurado."""
        # Arrange
        mock_get = mocker.patch("requests.get")
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Test Vendor"
        mock_get.return_value = mock_response
        
        service = MacVendorService()
        
        # Act
        service.get_vendor("00:11:22:33:44:55")
        
        # Assert
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["timeout"] == 2
    
    def test_get_vendor_strips_whitespace(self, mocker):
        """Elimina espacios en blanco de la respuesta."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "  Apple, Inc.  \n"
        mocker.patch("requests.get", return_value=mock_response)
        
        service = MacVendorService()
        
        # Act
        result = service.get_vendor("00:1A:2B:3C:4D:5E")
        
        # Assert
        assert result == "Apple, Inc."
    
    def test_get_vendor_multiple_different_macs(self, mocker):
        """Maneja múltiples MACs diferentes correctamente."""
        # Arrange
        def mock_get_side_effect(url, timeout):
            if "00:11:22" in url:
                response = Mock()
                response.status_code = 200
                response.text = "Vendor A"
                return response
            elif "AA:BB:CC" in url:
                response = Mock()
                response.status_code = 200
                response.text = "Vendor B"
                return response
        
        mocker.patch("requests.get", side_effect=mock_get_side_effect)
        service = MacVendorService()
        
        # Act
        result1 = service.get_vendor("00:11:22:33:44:55")
        result2 = service.get_vendor("AA:BB:CC:DD:EE:FF")
        
        # Assert
        assert result1 == "Vendor A"
        assert result2 == "Vendor B"
        assert len(service.cache) == 2
