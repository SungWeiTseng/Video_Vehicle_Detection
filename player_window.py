from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, \
    QStyle

from UI_function import MainUIFunction, VideoFrameGrabber


class ReidWindow(QWidget):
    def __init__(self, mainWindow):
        super(ReidWindow, self).__init__()

        self.setWindowTitle("Vehicle ReID Result")
        self.setGeometry(350, 100, 700, 500)

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.black)
        self.setPalette(palette)

        self.mainWindow = mainWindow

    def init_ui(self):
        self.resultLabel = QLabel()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.gray)
        self.setPalette(palette)

        self.reidWindow = ReidWindow(self)
        self.UI_function = MainUIFunction(self)
        self.init_ui()
        # self.showFullScreen()
        self.show()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videowidget = QVideoWidget()
        self.openBtn = QPushButton('Open Video')
        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        hboxLayout.addWidget(self.openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        self.imgLabel = QLabel(self)

        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(20, 20, 20, 20)
        vboxLayout.addWidget(self.imgLabel)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)
        self.grabber = VideoFrameGrabber(self)
        self.mediaPlayer.setVideoOutput(self.grabber)

        self.UI_function.set_function()
