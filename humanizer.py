import time
import random
import numpy as np
import pyautogui

# Desactivar fail-safe directo para manejarlo nosotros
pyautogui.FAILSAFE = True 

def human_delay(min_sec=0.1, max_sec=0.5):
    """Espera un tiempo aleatorio basado en una distribución normal."""
    mu = (min_sec + max_sec) / 2
    sigma = (max_sec - min_sec) / 6
    delay = random.gauss(mu, sigma)
    time.sleep(max(min_sec, min(max_sec, delay)))

def move_mouse_humanized(x, y, duration_base=0.5):
    """Mueve el ratón en una trayectoria curva y con velocidad variable."""
    start_x, start_y = pyautogui.position()
    
    # Añadimos un poco de 'ruido' al destino para no ser exactos
    target_x = x + random.randint(-2, 2)
    target_y = y + random.randint(-2, 2)
    
    # Generar puntos intermedios para una curva de Bézier simple
    control_x = (start_x + target_x) / 2 + random.randint(-50, 50)
    control_y = (start_y + target_y) / 2 + random.randint(-50, 50)
    
    steps = random.randint(15, 30)
    for i in range(steps + 1):
        t = i / steps
        # Ecuación cuadrática de Bézier
        curr_x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * target_x
        curr_y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * target_y
        
        pyautogui.moveTo(curr_x, curr_y)
        # Pequeña variación en el tiempo entre pasos
        time.sleep(random.uniform(0.001, 0.005))

def click_humanized(x=None, y=None, button='left'):
    """Realiza un clic con movimientos previos y delays humanos."""
    if x is not None and y is not None:
        move_mouse_humanized(x, y)
    
    human_delay(0.05, 0.15)
    pyautogui.mouseDown(button=button)
    human_delay(0.05, 0.1) # Simula presión física
    pyautogui.mouseUp(button=button)
    human_delay(0.1, 0.3)

def type_humanized(text):
    """Escribe texto con intervalos aleatorios entre teclas."""
    for char in text:
        pyautogui.write(char)
        human_delay(0.05, 0.2) # Ritmo de escritura humano
