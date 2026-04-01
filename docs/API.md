# API Endpoints (Flask)

El núcleo Backend se aloja en `http://localhost:5000/` y expone los siguientes endpoints para el frontend y el agente interno:

### Para el Frontend Web `(app.js)`

- `POST /action`
  Payload JSON: `{"action": "...", "text": "..."}`
  Ejecuta acciones basadas en `action`:
  - `start_agent`: Hace fork o spawn a `agent_core.py`.
  - `panic`: Encuentra el proceso del agente y le hace un `terminate` inmediato (Cierra el script de control también en caso de fallos).
  - `think`: Es el chat central. Parsea el `text`. Si el texto incluye intenciones de agresión (`mata`, `ataca`), fija ese texto como el Comando Persistente y devuelve una confirmación genérica. Si no, arranca `preguntar.ps1` llamando a `deepseek-r1` para asesoramiento general.

- `GET /stream`
  **Método MJPEG**. Un feed perpetuo multipart que escanea el monitor vía `mss` y expone los fotogramas sin compresión dura de forma raw para que un tag HTML `<img src="/stream">` la dibuje a +30FPS como visor.

- `GET /get_log`
  Retorna el estado actual de la telemetría del robot interno `{"thought": "...", "latency": 1.25}`.

### Para uso Interno del Agente `(agent_core.py)`

- `POST /log`
  Usado por el bucle del agente esbirro para actualizar el dashboard web de sus latencias y última decisión sobre lo que ve en la pantalla.
- `GET /get_command`
  Retorna el comando agresivo marcado en verde. Cuando está nulo, el Agente no gastará VRAM procesando.
- `POST /clear_command`
  Reinicia a `None` el foco bélico. Usado por la IA cuando dictamina que la acción ya está cumplida para volver a estado pasivo.
