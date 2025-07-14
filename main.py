import sys
from PySide6.QtWidgets import QApplication
from gui import MicroscopeGUI

def main():
    app = QApplication(sys.argv)
    window = MicroscopeGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()