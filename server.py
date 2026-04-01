from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os
import json
import cv2
import mss
import numpy as np
import time

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTROL_SCRIPT = os.path.join(BASE_DIR, "control.py")
AGENT_SCRIPT = os.path.join(BASE_DIR, "agent_core.py")

# Datos persistentes en memoria del servidor
agent_process = None
last_log = {"thought": "En espera...", "latency": 0}
last_command = None # Nueva orden pendiente (ej: "Ataca escorpiones")

@app.route('/log', methods=['POST'])
def save_log():
    global last_log
    last_log = request.json
    return jsonify({"success": True})

@app.route('/get_log', methods=['GET'])
def get_log():
    return jsonify(last_log)

@app.route('/get_command', methods=['GET'])
def get_command():
    return jsonify({"command": last_command})

@app.route('/clear_command', methods=['POST'])
def clear_command():
    global last_command
    last_command = None
    return jsonify({"success": True})

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1] 
        while True:
            try:
                img = sct.grab(monitor)
                frame = np.array(img)
                if frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                # Encode a JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(0.04) 
            except: break

@app.route('/stream')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/action', methods=['POST'])
def run_action():
    global agent_process
    data = request.json
    action = data.get('action')
    
    # PROTOCOLO DE PÁNICO
    if action == "panic":
        if agent_process:
            print(">>> DETENIENDO AGENTE POR PANICO...")
            agent_process.terminate()
            agent_process.wait() # Esperar a que termine de verdad
            agent_process = None
        return jsonify({"success": True, "message": "Pánico activado. Agente detenido."})

    # ACTIVAR AGENTE
    elif action == "start_agent":
        if not agent_process:
            agent_process = subprocess.Popen(["python", AGENT_SCRIPT])
            return jsonify({"success": True, "message": "Esbirro del Terror liberado."})
        return jsonify({"success": False, "message": "El esbirro ya está activo."})

    # CONSULTA A IA (PARA EL CHAT)
    elif action == "think":
        global last_command
        prompt = data.get('text', '').lower()
        
        # Filtro para DETENER el ataque persistente
        if any(word in prompt for word in ["para", "detente", "stop", "quieto", "espera"]):
            last_command = None
            return jsonify({"success": True, "output": "Orden de cese al fuego recibida. El Esbirro vuelve a modo pasivo."})
        
        # Filtro para detectar intención de ataque (PERSISTENTE)
        if any(word in prompt for word in ["ataca", "mata", "combate", "escorpion", "fuego", "limpia", "objetivo"]):
            last_command = prompt
            return jsonify({"success": True, "output": f"Fijando objetivo: '{prompt}'. El Esbirro atacará a todo lo que vea hasta que la zona esté limpia o digas 'PARE'."})

        # Para otras consultas, usamos el asesor
        system_context = "Responde como un asistente experto de World of Warcraft Vanilla. "
        cmd = ["powershell", "-File", os.path.join(BASE_DIR, "preguntar.ps1"), "-Prompt", system_context + prompt]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return jsonify({"success": True, "output": result.stdout.strip()})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Acción no reconocida."})

if __name__ == '__main__':
    print(">>> SERVIDOR DE MANDO: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
