"""
Fixtures compartidas para los tests del Monitor de Red.
Proporciona mocks para dependencias externas (scapy, psutil, socket).
"""

import pytest
from unittest.mock import Mock, MagicMock
from collections import namedtuple


@pytest.fixture
def mock_socket(mocker):
    """Mock de socket para tests de NetworkScanner."""
    mock_sock = MagicMock()
    mock_sock.getsockname.return_value = ("192.168.1.100", 12345)
    mocker.patch("socket.socket", return_value=mock_sock)
    return mock_sock


@pytest.fixture
def mock_psutil_counters():
    """Mock de psutil.net_io_counters para tests de NetworkSensor."""
    # Creamos un namedtuple similar al que retorna psutil
    NetIOCounters = namedtuple(
        "NetIOCounters",
        ["bytes_sent", "bytes_recv", "packets_sent", "packets_recv"]
    )
    return NetIOCounters


@pytest.fixture
def mock_scapy_response():
    """Mock de respuesta de scapy.srp para tests de NetworkScanner."""
    # Simulamos una respuesta ARP exitosa
    mock_packet = Mock()
    mock_packet.psrc = "192.168.1.1"  # IP source
    mock_packet.hwsrc = "aa:bb:cc:dd:ee:ff"  # MAC source
    
    # scapy.srp retorna una tupla (answered, unanswered)
    # answered es una lista de tuplas (request, response)
    answered = [(Mock(), mock_packet)]
    unanswered = []
    
    return (answered, unanswered)


@pytest.fixture
def mock_flet_chart_point(mocker):
    """Mock de flet_charts.LineChartDataPoint para tests de DataManager."""
    mock_point_class = mocker.patch("flet_charts.LineChartDataPoint")
    
    def create_point(x, y):
        point = Mock()
        point.x = x
        point.y = y
        return point
    
    mock_point_class.side_effect = create_point
    return mock_point_class
