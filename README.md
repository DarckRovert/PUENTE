# ESBIRRO DEL TERROR - NÚCLEO DE MANDO (PUENTE)

Puente es un sistema de asistencia e Inteligencia Artificial autónoma local diseñado para interactuar con World of Warcraft Vanilla (particularmente Turtle WoW). Integra capacidades MLLM (Modelos de Lenguaje Locales Multimodales) a través de Ollama, permitiéndole "ver" la pantalla y tomar decisiones en tiempo real sobre el combate u otras acciones usando `moondream` o interpretar dudas de los jugadores mediante un chat inteligente soportado por `deepseek-r1`.

![Dashboard Screenshot](https://via.placeholder.com/800x450.png?text=Esbirro+Dashboard)

## Características
- **Visión Mágica Ojo del Vacío:** Captura de pantalla a alto rendimiento (`mss` + `OpenCV`) para observar el entorno del juego en tiempo real (visión directa para el navegador y para la IA).
- **Esbirro Fast-Track (Moondream):** Un agente autónomo que procesa imágenes del juego junto a una instrucción persistente (ej. "Ataca escorpiones") y desencadena acciones de ratón/teclado si confirma amenazas visuales.
- **Protocolo de Input Humanizado:** El movimiento del ratón y el clic no son instantáneos ni mecánicos; utilizan curvas de Bézier e intervalos de latencia gaussianos para emular el input de un humano real y evadir filtros anti-bot básicos.
- **Dashboard Web de Control Local:** Interfaz 100% web gestionada por Flask, sin dependencias a servicios externos en la nube, resguardando la telemetría y ejecución.
- **Botón de Pánico:** Cancelación inmediata y detención segura del proceso de agente autónomo.

## Requisitos del Sistema
- **Sistema Operativo:** Windows 10/11
- **Python:** 3.10 o superior
- **Ollama:** Instalado y ejecutándose en `http://localhost:11434`
- **Juego:** World of Warcraft Vanilla o cliente compatible abierto en modo Ventana o Ventana Maximizada.

**Modelos de IA requeridos en Ollama:**
```bash
ollama pull moondream:latest
ollama pull deepseek-r1:8b
```

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/DarckRovert/PUENTE.git
   cd PUENTE
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Cómo Iniciar
1. Asegúrate de tener **Ollama** ejecutándose en segundo plano.
2. Haz doble clic en el archivo **`ARRANCAR_ESBIRRO.bat`**.
   - Esto abrirá de forma automática el servidor Flask y la UI del navegador (`index.html`).
3. Para iniciar la cacería, asegúrate de tener WoW en foco y haz clic en **"LIBERAR ESBIRRO"** en la web.

## Documentación Técnica
Revisa la carpeta `/docs` para entender mejor cómo funciona cada módulo por dentro:
- [Arquitectura de Datos y Componentes (`docs/ARCHITECTURE.md`)](docs/ARCHITECTURE.md)
- [Ciclo de Vida del Agente AI (`docs/AGENT.md`)](docs/AGENT.md)
- [API Endpoints de Flask (`docs/API.md`)](docs/API.md)
- [Comandos de Chat y Control (`docs/COMMANDS.md`)](docs/COMMANDS.md)

## Seguridad
- No exponer el puerto 5000 a internet público, ya que permite la ejecución de inputs que controlan los dispositivos primarios del PC.
- Usa esto bajo tu propia responsabilidad. El autor no se hace responsable del uso de esta herramienta en servidores oficiales.
