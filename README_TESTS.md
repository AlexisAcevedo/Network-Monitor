# 🧪 Guía de Testing - Monitor de Red

## Descripción

Esta guía explica cómo ejecutar y mantener la suite de tests del proyecto Monitor de Red.

---

## 📦 Instalación de Dependencias

Instala las dependencias de testing:

```bash
pip install -r requirements.txt
```

Las dependencias de testing incluyen:
- `pytest>=8.0.0` - Framework de testing
- `pytest-cov>=4.1.0` - Generación de reportes de cobertura
- `pytest-mock>=3.12.0` - Utilidades para mocking

---

## 🚀 Ejecución de Tests

### Ejecutar todos los tests

```bash
pytest tests/ -v
```

**Salida esperada:**
```
tests/test_scanner.py::TestNetworkScannerInit::test_init_creates_target_ip PASSED
tests/test_scanner.py::TestGetLocalRange::test_get_local_range_success PASSED
...
======================== 39 passed in 2.45s ========================
```

### Ejecutar tests de un módulo específico

```bash
# Solo NetworkScanner
pytest tests/test_scanner.py -v

# Solo NetworkSensor
pytest tests/test_sensor.py -v

# Solo DataManager
pytest tests/test_data_manager.py -v
```

### Ejecutar un test específico

```bash
pytest tests/test_scanner.py::TestGetLocalRange::test_get_local_range_success -v
```

---

## 📊 Reportes de Cobertura

### Generar reporte de cobertura en terminal

```bash
pytest tests/ --cov=core --cov-report=term
```

**Salida esperada:**
```
---------- coverage: platform win32, python 3.x -----------
Name                      Stmts   Miss  Cover
---------------------------------------------
core\__init__.py              0      0   100%
core\data_manager.py         35      2    94%
core\scanner.py              28      1    96%
core\sensor.py               20      0   100%
---------------------------------------------
TOTAL                        83      3    96%
```

### Generar reporte HTML interactivo

```bash
pytest tests/ --cov=core --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador para ver:
- Cobertura por archivo
- Líneas cubiertas/no cubiertas
- Análisis detallado de cada módulo

---

## 🎯 Estructura de Tests

```
tests/
├── __init__.py              # Paquete de tests
├── conftest.py              # Fixtures compartidas
├── test_scanner.py          # 11 tests de NetworkScanner
├── test_sensor.py           # 14 tests de NetworkSensor
└── test_data_manager.py     # 14 tests de DataManager
```

**Total: 39 tests unitarios**

---

## 🧩 Cobertura por Módulo

| Módulo | Tests | Cobertura Objetivo |
|--------|-------|-------------------|
| `NetworkScanner` | 11 | ≥ 80% |
| `NetworkSensor` | 14 | ≥ 85% |
| `DataManager` | 14 | ≥ 90% |

---

## 🔧 Fixtures Disponibles

Las fixtures en `conftest.py` proporcionan mocks para dependencias externas:

### `mock_socket`
Mock de `socket.socket` para tests de `NetworkScanner`.

```python
def test_example(mock_socket):
    scanner = NetworkScanner()
    # socket está mockeado, no hace conexiones reales
```

### `mock_psutil_counters`
Namedtuple compatible con `psutil.net_io_counters`.

```python
def test_example(mock_psutil_counters):
    counters = mock_psutil_counters(bytes_sent=1000, bytes_recv=2000, ...)
```

### `mock_scapy_response`
Mock de respuesta ARP de scapy.

```python
def test_example(mock_scapy_response):
    # Simula dispositivos encontrados sin escaneo real
```

### `mock_flet_chart_point`
Mock de `flet_charts.LineChartDataPoint`.

```python
def test_example(mock_flet_chart_point):
    manager = DataManager()
    # Puntos gráficos están mockeados
```

---

## ✅ Agregar Nuevos Tests

### Patrón AAA (Arrange-Act-Assert)

Todos los tests siguen este patrón:

```python
def test_nueva_funcionalidad(mocker):
    # Arrange - Preparar datos y mocks
    mock_data = mocker.patch("module.function", return_value=123)
    
    # Act - Ejecutar función bajo prueba
    result = funcion_a_testear()
    
    # Assert - Verificar resultado
    assert result == 123
    mock_data.assert_called_once()
```

### Ejemplo completo

```python
class TestNuevaFuncionalidad:
    """Tests de nueva funcionalidad."""
    
    def test_caso_feliz(self, mocker):
        """Descripción del caso feliz."""
        # Arrange
        mock_dep = mocker.patch("core.scanner.dependency")
        mock_dep.return_value = "expected"
        
        # Act
        result = nueva_funcion()
        
        # Assert
        assert result == "expected"
    
    def test_manejo_error(self, mocker):
        """Descripción del manejo de error."""
        # Arrange
        mock_dep = mocker.patch("core.scanner.dependency")
        mock_dep.side_effect = Exception("Error")
        
        # Act
        result = nueva_funcion()
        
        # Assert
        assert result is None  # O el comportamiento esperado
```

---

## 🐛 Debugging de Tests

### Ver output detallado

```bash
pytest tests/ -v -s
```

La opción `-s` muestra los prints dentro de los tests.

### Ejecutar solo tests que fallaron

```bash
pytest tests/ --lf
```

### Detener en el primer fallo

```bash
pytest tests/ -x
```

---

## 📋 Checklist de Calidad

Antes de hacer commit, verifica:

- [ ] Todos los tests pasan: `pytest tests/ -v`
- [ ] Cobertura ≥ 80%: `pytest tests/ --cov=core --cov-report=term`
- [ ] Sin warnings: `pytest tests/ -v --tb=short`
- [ ] Tests aislados (sin dependencias externas)
- [ ] Nombres descriptivos de tests
- [ ] Docstrings en clases de test

---

## 🎓 Recursos

- [Documentación de pytest](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)

---

## 💡 Tips

1. **Ejecuta tests frecuentemente** durante el desarrollo
2. **Usa `-k` para filtrar tests**: `pytest -k "scanner" -v`
3. **Revisa el reporte HTML** para encontrar líneas sin cobertura
4. **Mockea dependencias externas** para tests rápidos y confiables
5. **Escribe tests antes de refactorizar** (TDD)
