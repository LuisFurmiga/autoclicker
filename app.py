import sys
from controllers.app_controller import AppController


def main():
    controller = AppController()
    controller.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Evita crash silencioso ao empacotar (PyInstaller)
        print(f"Fatal error: {e}")
        sys.exit(1)
