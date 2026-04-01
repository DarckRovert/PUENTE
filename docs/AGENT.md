# Ciclo del Agente Core (`agent_core.py`)

El Esbirro del Terror (`agent_core.py`) es un proceso independiente invocado por el servidor de comando que evalúa fotogramas rápidos del juego. Su objetivo no es ser un asistente de chat, sino un detector de visión por computadora reactivo.

## Ciclo por Ticks
El archivo funciona sobre un `while ACTIVE:` que ejecuta este flujo:

1. **Fetch de Objetivos:**
   El agente hace ping local (`http://localhost:5000/get_command`).
   - ¿Hay orden de ataque? -> Paso 2
   - No hay orden de combate -> Sleep y re-intenta (estado `IDLE`).
2. **Captura Visual Rápida:**
   Vía `mss` extrae una captura del juego. Para evitar latencia pesada de codificación, `OpenCV` redimensiona el fotograma a 320x180.
3. **Consulta Cognitiva:**
   Envía el fotograma con el prompt precalculado junto a la palabra a buscar (ej: `"ataca escorpiones" -> prompt("is there escorpiones? answer ACTION o WAIT")`)
4. **Respuesta Rápida y Acción:**
   El modelo `moondream` debería resolver de forma sub-segundo la consulta. Si su output es `ACTION`, llama asíncronamente a `control.py` inyectando pulsaciones.
5. **Feed Telescópico:**
   Publica la respuesta recibida, latencia y telemetría en el endpoint `/log` de Flask para que el Dashboard la grafique.

## Parámetros Ocultos
A nivel de código en `agent_core.py`:
- **Timeout**: Está agresivamente corto en `timeout=12` para IA y `timeout=0.5` para la telemétrica, matando procesos que demoren mucho e ignorando el retardo para forzar celeridad.
- **Temperatura**: Configurada a `0` para que la respuesta de Moondream sea completamente binaria y determinística, limitando la "creatividad" e incrementando asertividad de visión por ML.
