import mss
import requests
import base64
import time
import subprocess
import os
import json
import cv2
import numpy as np

# Configuración Optimizada
OLLAMA_URL = "http://localhost:11434/api/generate"
SERVER_URL = "http://localhost:5000"
MODEL = "moondream:latest" 
ACTIVE = True

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
        img_small = cv2.resize(img_np, (320, 180))
        _, buffer = cv2.imencode('.jpg', img_small, [cv2.IMWRITE_JPEG_QUALITY, 50])
        return base64.b64encode(buffer).decode('utf-8')

def consult_ia(image_b64, command):
    # Prompt ultra-simplificado para reacción relámpago
    prompt = f"WORLD: WoW game. ORDER: '{command}'. Is there an enemy for this? ONLY say 'ACTION' if yes, or 'WAIT' if none."
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
        "keep_alive": -1,
        "options": { "temperature": 0, "num_predict": 10 }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=12)
        res_text = response.json().get('response', '').strip()
        return res_text
    except: return "ERROR"

def check_for_command():
    try:
        resp = requests.get(f"{SERVER_URL}/get_command", timeout=1)
        return resp.json().get('command')
    except: return None

def clear_command():
    try: requests.post(f"{SERVER_URL}/clear_command", timeout=1)
    except: pass

def execute_attack():
    # El ritual de ataque del Sequito del Terror
    control_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "control.py")
    subprocess.run(["python", control_script, "--action", "type", "--text", "1"])
    time.sleep(0.1)  # Más rápido
    subprocess.run(["python", control_script, "--action", "type", "--text", "4"])

def main_loop():
    print(f">>> MONITOR DEL VACÍO ACTIVO ({MODEL})")
    while ACTIVE:
        start_time = time.time()
        
        # 1. ¿Hay una orden pendiente?
        command = check_for_command()
        
        if command:
            img_b64 = capture_screen()
            decision = consult_ia(img_b64, command)
            
            # ATENCIÓN: Logueamos la respuesta RAW para diagnóstico
            thought = f"PENSAMIENTO: '{decision}' | ORDEN: {command}"
            
            if "ACTION" in decision.upper():
                execute_attack()
            
        else:
            thought = "En espera de órdenes..."
            decision = "IDLE"

        # 3. Telemetría
        elapsed = time.time() - start_time
        try:
            requests.post(f"{SERVER_URL}/log", json={
                "thought": thought, 
                "latency": elapsed
            }, timeout=0.5)
        except: pass
        
        time.sleep(0.3)

if __name__ == "__main__":
    main_loop()
