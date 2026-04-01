# Arquitectura del Sistema PUENTE

Este documento expone cómo se comunican las distintas partes del sistema PUENTE. 
Es una arquitectura asíncrona liderada por Flask que orquesta la captura de imagen, las solicitudes locales a modelos de ML y la ejecución de ratón/teclado.

## Diagrama de Componentes

```mermaid
graph TD
    UI[Frontend HTML/JS] -->|AJAX Polling / WebSocket simulado| F(Flask Server - server.py)
    
    F -->|Subprocess| A(Agente Ojo del Vacío - agent_core.py)
    F -->|PowerShell| PS(Asistente Chat - preguntar.ps1)
    
    PS -->|HTTP req| O[Ollama Local API]
    
    A -->|1. Polling Orden Activa /get_command| F
    A -->|2. Captura Imagen| MSS(mss + OpenCV)
    A -->|3. Consulta| O
    A -->|4. Si detecta objetivo| C(Ejecutor - control.py)
    A -->|5. Telemetría /log| F
    
    C --> H(humanizer.py)
    H -->|Input de Simulación| OS(PyAutoGUI Win32)
```

## Módulos Core

1. **`server.py`**: El backend en Flask. Guarda en memoria ram el comando actual (`last_command`), sirve las páginas, maneja el Pánico Absoluto (matando subprocesos) e interconecta todas las piezas.
2. **`agent_core.py`**: El bucle infinito del Esbirro. No hace nada hasta que el servidor recibe de la web una ORDEN DE COMBATE (guardado en Flask). Ahí empieza a ciclar sobre capturas de pantalla de bajo peso que se mandan a Moondream por local HTTP junto con el prompt.
3. **`control.py` & `humanizer.py`**: Aislados en un script `argparse`. Esto facilita invocar ratón/teclado de forma humana desde PowerShell, JS, Agente u otras interrupciones externas sin acoplarse y arrancar un ecosistema gordo de imports cruzados.
4. **`app.js`**: Telemetría reactiva en el frontend evaluando logs en tiempo real (`setInterval`).
