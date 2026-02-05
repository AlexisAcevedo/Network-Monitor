# Manual de Usuario - Monitor de Red

Bienvenido al **Monitor de Red**, tu herramienta todo-en-uno para gestionar y probar tu red local.

## 🚀 Inicio Rápido

1.  **Ejecutar la aplicación**:
    Dobble click en el acceso directo o ejecuta `python main.py` desde la terminal.
2.  **Permisos**:
    Al usar funcionalidades de red (ARP, Speedtest), es posible que Windows solicite permisos de Firewall la primera vez. Acéptalos para garantizar el funcionamiento.

---

## 📊 1. Dashboard de Monitor (Monitor)

Es la pantalla principal que verás al iniciar.

-   **Gráfico en Tiempo Real**: Muestra el consumo de ancho de banda (Bajada en Azul, Subida en Naranja).
-   **Velocímetro**: Muestra la velocidad actual instantánea.
-   **Estadísticas**: Panel lateral con el consumo total de la sesión y picos máximos.
-   **Alertas**: Puedes configurar un umbral (en MB/s). Si el tráfico supera ese límite, recibirás una notificación de Windows.

**Tip**: Úsalo para detectar qué programas están consumiendo tu internet en segundo plano.

---

## 📡 2. Escáner de Dispositivos (Scanner)

Aquí puedes ver quién está conectado a tu WiFi o red cableada.

1.  Click en **"Scan Network"**.
2.  Espera unos segundos mientras se analiza la red.
3.  Aparecerá una lista con:
    -   **IP Address**: La "dirección" del dispositivo.
    -   **MAC Address**: El identificador único físico.
    -   **Vendor**: El fabricante (ej. Apple, Samsung, Dell).

### Escaneo de Puertos 🔍
Una vez detectados los dispositivos, puedes analizar su seguridad:
1.  Marca la casilla ☑️ al lado de uno o varios dispositivos.
2.  Selecciona el **Scan Mode**:
    -   *Quick*: Revisa los 20 puertos más comunes (Web, FTP, SSH).
    -   *Standard*: Revisa 100 puertos frecuentes.
    -   *Full*: Escaneo profundo (lento).
3.  Click en **"Scan Ports"**.
4.  Se abrirá una ventana mostrando qué puertos están "ABIERTOS" en esos dispositivos.

---

## 🗺️ 3. Topología de Red (Topology)

Una representación visual de tu red.

-   Al entrar, el sistema escanea automáticamente.
-   Verás al **Router/Gateway** en la parte superior (icono CYAN).
-   Debajo, conectados por líneas, todos los dispositivos detectados.
-   El sistema intenta adivinar qué son: Teléfonos 📱, PCs 💻, Impresoras 🖨️, etc.

**Uso**: Ideal para tener un mapa mental rápido de la estructura de tu red.

---

## 🚀 4. Speedtest

Prueba tu velocidad real de conexión a Internet (no solo la de tu red local).

1.  Click en **"Run Test"**.
2.  La aplicación contactará con el servidor más cercano.
3.  Verás:
    -   **Ping**: Latencia (menor es mejor, ideal para juegos).
    -   **Download**: Velocidad de descarga (streaming, descargas).
    -   **Upload**: Velocidad de subida (videollamadas, enviar archivos).

> **Nota**: Este test consume datos reales de tu plan de internet.

---

## ❓ Solución de Problemas

**No detecto dispositivos:**
-   Asegúrate de tener instalado **Npcap** (en modo WinPcap compatible) si estás en Windows. Es necesario para que el escáner ARP funcione.
-   Verifica que no estás conectado a una VPN, ya que esto oculta tu red local.

**El gráfico no se mueve:**
-   Verifica tu conexión a internet.
-   Reinicia la aplicación.

**Speedtest falla:**
-   Requiere conexión activa a internet. Si tienes firewall corporativo, puede bloquear la conexión.
