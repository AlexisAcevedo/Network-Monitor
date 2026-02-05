# Monitor de Red

Aplicación de escritorio moderna construida con Python y Flet para monitorear el tráfico de red en tiempo real y escanear dispositivos conectados en la red local.

> **Nota:** Este proyecto está sujeto a futuras implementaciones y mejoras.

## Características Principales

-   **Monitor de Tráfico en Tiempo Real**: Visualiza la velocidad de descarga y subida con gráficos dinámicos.
-   **Speedtest Integrado**: Mide tu velocidad real de internet (bajada, subida y ping) usando servidores cercanos.
-   **Dashboard de Topología**: Mapa visual interactivo de tu red que clasifica dispositivos automáticamente (PC, Móvil, Router, etc.).
-   **Escáner de Puertos Avanzado**: Analiza dispositivos conectador para detectar puertos abiertos (Modos: Quick, Standard, Full).
-   **Escáner de Dispositivos**: Identifica dispositivos conectados a tu red local (IP y MAC) mediante escaneo ARP.
-   **Interfaz Moderna**: UI limpia y responsiva con modo oscuro, barra lateral y notificaciones.

## Requisitos Previos

-   **Python 3.x** instalado.
-   **Npcap** (solo Windows): Necesario para que `scapy` funcione correctamente. [Descargar Npcap](https://npcap.com/#download) (asegúrese de marcar "Install Npcap in WinPcap API-compatible Mode").

## Instalación

1.  Clonar el repositorio o descargar el código.
2.  Crear un entorno virtual (recomendado):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para iniciar la aplicación, ejecute el archivo principal:

```bash
python main.py
```

### Navegación

-   **Monitor**: Pestaña principal que muestra el gráfico de tráfico.
-   **Escáner**: Buscador de dispositivos y escáner de puertos.
-   **Topología**: Visualización gráfica de la red en árbol.
-   **Speedtest**: Test de velocidad de internet.

## Estructura del Proyecto

```
Monitor de Red/
├── core/               # Lógica de negocio (Backend)
│   ├── sensor.py       # Lectura de tráfico (psutil)
│   ├── scanner.py      # Escaneo de red (scapy)
│   ├── speedtest_service.py # Servicio Speedtest
│   ├── device_classifier.py # Clasificación de dispositivos
│   ├── port_scanner.py # Escáner de puertos
│   └── data_manager.py # Gestión de datos
├── ui/                 # Interfaz de Usuario (Frontend)
│   ├── views/          # Pantallas (Monitor, Scanner, Speedtest, Topology)
│   ├── charts.py       # Componente de gráfico
│   ├── sidebar.py      # Menú lateral
│   └── layout.py       # Estructura base de la app
├── main.py             # Punto de entrada
└── requirements.txt    # Dependencias
```
