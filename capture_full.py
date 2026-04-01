import mss
import cv2
import numpy as np
import os

def capture_full_screen(output_path):
    try:
        with mss.mss() as sct:
            # Capturar el monitor principal (0 suele ser todo el escritorio)
            monitor = sct.monitors[1]
            img = sct.grab(monitor)
            img_np = np.array(img)
            if img_np.shape[2] == 4:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            
            cv2.imwrite(output_path, img_np)
            print(f"CAPTURE_FULL_SUCCESS: {output_path}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "full_screen.png")
    capture_full_screen(output_file)
