import sys

from PyQt5.QtWidgets import QApplication

from player_window import mainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())
