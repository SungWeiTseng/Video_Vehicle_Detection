import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QStyle, QSlider, QHBoxLayout, QVBoxLayout


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vehicle Detection")

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.black)
        self.setPalette(palette)

        self.init_ui()
        self.show()

    def show_mouse_press(self, event):
        print(f"[show_mouse_press] {event.x()}, {event.y()}, {event.button()}")

    def init_ui(self):
        self.openBtn = QPushButton('Open Video')
        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        hboxLayout.addWidget(self.openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        img = QImage("C:/Users/Tseng Sung Wei/Pictures/loss.png")
        img = QImage("D:/照片/43826.jpg")
        self.label = QLabel(self)

        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(20, 20, 20, 20)
        vboxLayout.addWidget(self.label)
        vboxLayout.addLayout(hboxLayout)
        self.label.setPixmap(QPixmap.fromImage(img))
        P = img.rect()
        # self.resize(P.width() + 100, P.height() + 100)
        self.setLayout(vboxLayout)
        self.label.mousePressEvent = self.show_mouse_press


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
