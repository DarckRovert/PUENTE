# Comandos y Directivas del Chat

El puente interconecta intenciones a través de palabras clave registradas en el backend y los modelos locales. Tú ordenas mediante la barra principal del Dashboard y el sistema decide a quién delegar tu orden.

### Comandos de "Asistencia de Conocimiento"
Si tu consulta **NO** contiene palabras de agresión, será respondida como chat puro.
- **Ejemplo**: *"¿Cuáles son las profesiones óptimas para Warlock lvl 10?"*
- **Reacción**: El payload entra a un script e invoca al modelo DeepSeek-R1 (Localizado). Funciona offline dictando conocimiento del juego.

### Directivas de Agresión (Protocolos Autónomos)
Si envías ciertas palabras, se activará el Esbirro de Visión Automática.

- **Filtros (Lanzan el agente a la acción)**:
  - `ataca`, `mata`, `combate`, `limpia`, `objetivo`
- **Comportamiento**: 
  - Al enviar *"Mata ese jabalí"* la UI responderá "Fijando objetivo".
  - El sistema de visión de Moondream entra en bucle y buscará jabalíes por la pantalla del WoW usando la cámara constante a latencias gaussianas. De encontrar coincidencias visuales, ejecutará la habilidad 1 y 4 (Las que están mapeadas en `agent_core.py > execute_attack()`).

### Directivas de Cancelación (Cese al fuego)
Para decirle al sistema que pare de gastar la GPU analizando el monitor si los monstruos murieron o quieres parar:

- **Filtros**:
  - `para`, `detente`, `stop`, `quieto`, `espera`
- **Reacción**:
  - Limpia la memoria del backend. El agente detiene la inspección binaria y apaga su ciclo activo, pasando a estado `IDLE` de ahorro de cómputo.

### Botón Rojo de Panel "PANIC"
A diferencia de los comandos `detente`, el pánico inmolativo rompe el hilo a nivel de Sistema Operativo (`process.terminate()`). Literalmente es para prevenir incidentes que escapen al `fail-safe` de PyAutoGUI o atascos del ML que saturen el buffer interno en iteraciones locas. Usarlo requiere volver a presionar "LIBERAR ESBIRRO".
