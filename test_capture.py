import pygetwindow as gw
import mss
import cv2
import numpy as np
import time
import os

def force_capture(title, output_path):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            print(f"WINDOW_NOT_FOUND: {title}")
            return
        
        win = windows[0]
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(1) # Esperar a que la ventana se dibuje
        
        with mss.mss() as sct:
            monitor = {
                "top": win.top,
                "left": win.left,
                "width": win.width,
                "height": win.height
            }
            img = sct.grab(monitor)
            img_np = np.array(img)
            if img_np.shape[2] == 4:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            
            cv2.imwrite(output_path, img_np)
            print(f"CAPTURE_SUCCESS: {output_path}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wow_real.png")
    force_capture("World of Warcraft", output_file)
