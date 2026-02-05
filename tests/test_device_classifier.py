"""
Tests para DeviceClassifier (core/device_classifier.py).
Verifica la clasificación correcta de dispositivos según MAC y Vendor.
"""

import pytest
from core.device_classifier import DeviceClassifier, DeviceType

class TestDeviceClassifier:
    """Tests de la clase DeviceClassifier."""
    
    def test_classify_router_by_gateway_ip(self):
        """Verifica que una IP que termina en .1 se clasifica como Router."""
        dtype = DeviceClassifier.classify(
            mac="aa:bb:cc:dd:ee:ff",
            vendor="Desconocido",
            ip="192.168.1.1"
        )
        assert dtype == DeviceType.ROUTER
    
    def test_classify_phone_by_vendor(self):
        """Verifica clasificación de teléfonos por vendor."""
        vendors = ["Samsung Electronics", "Apple", "Xiaomi Communications", "OnePlus"]
        
        for vendor in vendors:
            dtype = DeviceClassifier.classify(
                mac="aa:bb:cc:dd:ee:ff",
                vendor=vendor,
                ip="192.168.1.50"
            )
            assert dtype == DeviceType.PHONE
            
    def test_classify_pc_by_vendor(self):
        """Verifica clasificación de PCs por vendor."""
        vendors = ["Dell Inc.", "Hewlett Packard", "ASUSTek Computer", "Lenovo"]
        
        for vendor in vendors:
            dtype = DeviceClassifier.classify(
                mac="aa:bb:cc:dd:ee:ff",
                vendor=vendor,
                ip="192.168.1.20"
            )
            assert dtype == DeviceType.PC

    def test_classify_printer_by_vendor(self):
        """Verifica clasificación de impresoras."""
        vendors = ["Canon", "Epson", "Brother Industries"]
        
        for vendor in vendors:
            dtype = DeviceClassifier.classify(
                mac="aa:bb:cc:dd:ee:ff",
                vendor=vendor,
                ip="192.168.1.60"
            )
            assert dtype == DeviceType.PRINTER

    def test_classify_router_by_vendor(self):
        """Verifica clasificación de routers por vendor (si no es gateway)."""
        vendors = ["TP-Link", "Cisco Systems", "Netgear", "Ubiquiti Networks"]
        
        for vendor in vendors:
            dtype = DeviceClassifier.classify(
                mac="aa:bb:cc:dd:ee:ff",
                vendor=vendor,
                ip="192.168.1.254" # No es .1, pero es router por vendor
            )
            assert dtype == DeviceType.ROUTER

    def test_classify_unknown(self):
        """Verifica fallback a UNKNOWN."""
        dtype = DeviceClassifier.classify(
            mac="aa:bb:cc:dd:ee:ff",
            vendor="Fabricante Raro S.A.",
            ip="192.168.1.99"
        )
        assert dtype == DeviceType.UNKNOWN

    def test_classify_handles_missing_vendor(self):
        """Maneja vendor nulo o vacío."""
        dtype = DeviceClassifier.classify(
            mac="aa:bb:cc:dd:ee:ff",
            vendor=None,
            ip="192.168.1.99"
        )
        assert dtype == DeviceType.UNKNOWN
