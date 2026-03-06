import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from theme import MODERN_DARK_THEME

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(MODERN_DARK_THEME)
    window.show()
    sys.exit(app.exec_())