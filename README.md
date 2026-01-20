# Monitor de Red

Aplicación de escritorio moderna construida con Python y Flet para monitorear el tráfico de red en tiempo real y escanear dispositivos conectados en la red local.

> **Nota:** Este proyecto está sujeto a futuras implementaciones y mejoras.

## Características Principales

-   **Monitor de Tráfico en Tiempo Real**: Visualiza la velocidad de descarga y subida con gráficos dinámicos.
-   **Escáner de Dispositivos**: Identifica dispositivos conectados a tu red local (IP y MAC) mediante escaneo ARP.
-   **Interfaz Moderna**: UI limpia y responsiva con modo oscuro.

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
-   **Escáner**: Pestaña para buscar dispositivos en la red. Haga clic en el botón flotante para iniciar un escaneo.

## Estructura del Proyecto

```
Monitor de Red/
├── core/               # Lógica de negocio (Backend)
│   ├── sensor.py       # Lectura de tráfico (psutil)
│   ├── scanner.py      # Escaneo de red (scapy)
│   └── data_manager.py # Gestión de datos
├── ui/                 # Interfaz de Usuario (Frontend)
│   ├── views/          # Pantallas (Monitor, Scanner)
│   ├── charts.py       # Componente de gráfico
│   ├── sidebar.py      # Menú lateral
│   └── layout.py       # Estructura base de la app
├── main.py             # Punto de entrada
└── requirements.txt    # Dependencias
```
