# Plan: Network Monitor Feature Expansion

## Overview

Implementar 3 nuevas funcionalidades para el Monitor de Red:
1. **Speedtest** - Prueba de velocidad de internet usando servicio externo
2. **Dashboard Topología** - Visualización en árbol de dispositivos con íconos
3. **Monitor de Puertos** - Escaneo configurable de puertos abiertos

**Tipo de Proyecto:** Desktop App (Python + Flet)

---

## Success Criteria

| Feature | Criterio de Éxito |
|---------|-------------------|
| Speedtest | Muestra velocidad download/upload en Mbps y latencia en ms |
| Topología | Árbol visual con router arriba, dispositivos abajo, íconos correctos |
| Puertos | Usuario elige dispositivo(s) y tipo de scan, resultados en tabla |

---

## Tech Stack

| Componente | Tecnología | Razón |
|------------|------------|-------|
| Speedtest | `speedtest-cli` | API estable, servidores globales Ookla |
| Port Scan | `scapy` (existente) | Ya está en el proyecto, evita nueva dependencia |
| UI | Flet (existente) | Consistencia con app actual |
| Device Icons | Material Icons | Ya usados en la app |

---

## File Structure

```
Monitor de Red/
├── core/
│   ├── speedtest_service.py   [NEW] Lógica de speedtest
│   ├── port_scanner.py        [NEW] Escaneo de puertos
│   ├── device_classifier.py   [NEW] Clasificación de dispositivos
│   └── ... (existentes)
├── ui/
│   └── views/
│       ├── speedtest_view.py  [NEW] Vista de speedtest
│       ├── topology_view.py   [NEW] Vista de topología
│       └── ... (existentes)
├── main.py                    [MODIFY] Agregar nuevas vistas
└── requirements.txt           [MODIFY] Agregar speedtest-cli
```

---

## Fase 1: Speedtest 🚀

### Task 1.1: Servicio de Speedtest
**Agent:** backend-specialist | **Skill:** python-patterns

| Campo | Valor |
|-------|-------|
| INPUT | Ninguno (usa internet) |
| OUTPUT | `core/speedtest_service.py` con clase `SpeedtestService` |
| VERIFY | `pytest tests/test_speedtest.py` pasa |

**Funciones:**
- `run_test()` → dict con download_mbps, upload_mbps, ping_ms, server_name
- `get_best_server()` → selecciona servidor óptimo
- Manejo de errores de conexión

---

### Task 1.2: Vista de Speedtest
**Agent:** frontend-specialist | **Skill:** frontend-design

| Campo | Valor |
|-------|-------|
| INPUT | `SpeedtestService` funcionando |
| OUTPUT | `ui/views/speedtest_view.py` |
| VERIFY | Vista renderiza sin errores, botón ejecuta test |

**UI Elements:**
- Botón "Run Test" con estado loading
- 3 cards: Download, Upload, Ping
- Indicador de servidor usado
- Historial de últimos 5 tests (opcional)

---

### Task 1.3: Integración
**Agent:** frontend-specialist

| Campo | Valor |
|-------|-------|
| INPUT | Vista completa |
| OUTPUT | `main.py` y `sidebar.py` modificados |
| VERIFY | Nueva pestaña visible y funcional |

---

## Fase 2: Dashboard Topología 🗺️

### Task 2.1: Clasificador de Dispositivos
**Agent:** backend-specialist | **Skill:** python-patterns

| Campo | Valor |
|-------|-------|
| INPUT | MAC address, vendor name |
| OUTPUT | `core/device_classifier.py` |
| VERIFY | Clasifica correctamente PC, phone, router, printer, unknown |

**Lógica de clasificación:**
```python
# Por vendor name (keywords)
"Apple", "Samsung", "Xiaomi" → phone/tablet
"HP", "Canon", "Epson" → printer
"Cisco", "TP-Link", "Netgear" → router
"Dell", "Lenovo", "ASUS" → pc
# Gateway IP (.1) → router
```

---

### Task 2.2: Vista de Topología
**Agent:** frontend-specialist | **Skill:** frontend-design

| Campo | Valor |
|-------|-------|
| INPUT | Datos de scanner + clasificador |
| OUTPUT | `ui/views/topology_view.py` |
| VERIFY | Árbol renderiza con router arriba, dispositivos abajo |

**Estructura Visual:**
```
        🌐 Router (192.168.1.1)
              │
    ┌─────────┼─────────┐
    │         │         │
   💻 PC    📱 Phone   🖨️ Printer
```

**Iconos Material:**
- Router: `icons.ROUTER`
- PC: `icons.COMPUTER`
- Phone: `icons.PHONE_ANDROID`
- Printer: `icons.PRINT`
- Unknown: `icons.DEVICE_UNKNOWN`

---

### Task 2.3: Integración
**Agent:** frontend-specialist

| Campo | Valor |
|-------|-------|
| INPUT | Vista completa |
| OUTPUT | Sidebar actualizado |
| VERIFY | Pestaña "Topology" funciona |

---

## Fase 3: Monitor de Puertos 🔍

### Task 3.1: Scanner de Puertos
**Agent:** backend-specialist | **Skill:** python-patterns

| Campo | Valor |
|-------|-------|
| INPUT | IP objetivo, modo de scan |
| OUTPUT | `core/port_scanner.py` |
| VERIFY | Detecta puertos abiertos correctamente |

**Modos:**
| Modo | Puertos | Timeout |
|------|---------|---------|
| quick | Top 20 (22,80,443,3389...) | 0.5s |
| standard | Top 100 | 0.3s |
| full | 1-1024 | 0.1s |

**Output:** Lista de `{port, service_name, state}`

---

### Task 3.2: UI de Escaneo de Puertos
**Agent:** frontend-specialist | **Skill:** frontend-design

| Campo | Valor |
|-------|-------|
| INPUT | `PortScanner` funcionando |
| OUTPUT | Componente en `scanner_view.py` |
| VERIFY | Usuario puede elegir dispositivo(s) y modo |

**UI Elements:**
- Checkbox "Scan all devices" o lista de checkboxes por dispositivo
- Dropdown: Quick / Standard / Full
- Botón "Scan Ports"
- Tabla de resultados con columnas: Device, Port, Service, State

---

### Task 3.3: Integración
**Agent:** frontend-specialist

| Campo | Valor |
|-------|-------|
| INPUT | Componente completo |
| OUTPUT | `scanner_view.py` actualizado |
| VERIFY | Escaneo funciona end-to-end |

---

## Phase X: Verificación Final

### Checklist

```bash
# 1. Lint
python -m flake8 core/ ui/ --max-line-length=120

# 2. Tests
pytest tests/ -v

# 3. Runtime
python main.py
# → Verificar las 3 nuevas pestañas funcionan
```

### Rule Compliance
- [ ] Código limpio sin over-engineering
- [ ] Tests para cada nuevo módulo
- [ ] UI consistente con diseño existente
- [ ] Manejo de errores en todas las operaciones de red

---

## Workflow por Fase

```
FASE N:
  1. Implementar tasks
  2. Ejecutar tests
  3. Verificación manual
  4. ✅ Notificar al usuario
  5. ⏸️ Esperar commit del usuario
  6. Usuario confirma → Continuar Fase N+1
```

---

## Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Speedtest lento | Mostrar progress indicator, timeout de 60s |
| Port scan bloqueado por firewall | Advertencia en UI, skip dispositivos sin respuesta |
| Clasificación incorrecta de device | Fallback a "Unknown", permitir edición manual (futuro) |
| scapy requiere permisos admin | Documentar en README, manejar error gracefully |

---

## Dependencies

```txt
# Agregar a requirements.txt
speedtest-cli>=2.1.3
```

> **Nota:** `scapy` ya está instalado para el scanner existente.
