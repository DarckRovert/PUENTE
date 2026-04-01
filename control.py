import argparse
import humanizer
import vision
import pygetwindow as gw
import sys

def main():
    parser = argparse.ArgumentParser(description="Puente Pro Control CLI")
    parser.add_argument("--action", choices=["click", "type", "move", "find", "capture"], required=True)
    parser.add_argument("--x", type=int, help="Coordenada X destino")
    parser.add_argument("--y", type=int, help="Coordenada Y destino")
    parser.add_argument("--text", type=str, help="Texto para escribir")
    parser.add_argument("--title", type=str, help="Título de la ventana")
    default_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_action.png")
    parser.add_argument("--output", type=str, default=default_output, help="Path de salida para captura")

    args = parser.parse_args()

    try:
        if args.action == "find":
            windows = gw.getWindowsWithTitle(args.title or "")
            if windows:
                win = windows[0]
                print(f"WINDOW_FOUND|{win.title}|{win.left}|{win.top}|{win.width}|{win.height}")
            else:
                print("WINDOW_NOT_FOUND")

        elif args.action == "capture":
            path, err = vision.capture_window(args.title, args.output)
            if err:
                print(f"CAPTURE_ERROR|{err}")
            else:
                print(f"CAPTURE_SUCCESS|{path}")

        elif args.action == "click":
            if args.x is not None and args.y is not None:
                humanizer.click_humanized(args.x, args.y)
                print(f"CLICK_SUCCESS|{args.x},{args.y}")
            else:
                print("ERROR: Faltan coordenadas X, Y para clic.")

        elif args.action == "move":
            if args.x is not None and args.y is not None:
                humanizer.move_mouse_humanized(args.x, args.y)
                print(f"MOVE_SUCCESS|{args.x},{args.y}")

        elif args.action == "type":
            if args.text:
                humanizer.type_humanized(args.text)
                print(f"TYPE_SUCCESS|{len(args.text)} chars")

    except Exception as e:
        print(f"CRITICAL_ERROR|{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
