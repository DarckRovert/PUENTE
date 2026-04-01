import mss
import pygetwindow as gw
import numpy as np
import cv2
import os

def capture_window(window_title, output_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_capture.png")):
    """Captura una ventana específica por título y guarda la imagen."""
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            return None, f"Ventana '{window_title}' no encontrada."
        
        win = windows[0]
        # Aseguramos coordenadas dentro de la pantalla
        with mss.mss() as sct:
            monitor = {
                "top": win.top,
                "left": win.left,
                "width": win.width,
                "height": win.height
            }
            img = sct.grab(monitor)
            # Convertir a formato compatible con OpenCV
            img_np = np.array(img)
            # Eliminar canal alpha si existe
            if img_np.shape[2] == 4:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            
            cv2.imwrite(output_path, img_np)
            return output_path, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    # Test simple con una ventana conocida
    path, err = capture_window("Notepad")
    if err:
        print(f"Error: {err}")
    else:
        print(f"Captura guardada en: {path}")
