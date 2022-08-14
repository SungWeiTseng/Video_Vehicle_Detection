import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, \
    QFileDialog, QStyle


class UI_function:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.main_window, "Open Video")

        if filename != '':
            self.main_window.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.main_window.playBtn.setEnabled(True)

    def play_video(self):
        if self.main_window.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.main_window.mediaPlayer.pause()
        else:
            self.main_window.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.main_window.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.main_window.playBtn.setIcon(
                self.main_window.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.main_window.playBtn.setIcon(
                self.main_window.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.main_window.slider.setValue(position)

    def duration_changed(self, duration):
        self.main_window.slider.setRange(0, duration)

    def set_position(self, position):
        self.main_window.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.main_window.playBtn.setEnabled(False)
        self.main_window.label.setText("Error: " + self.main_window.mediaPlayer.errorString())

    def show_mouse_press(self, event):
        self.main_window.label.setText(f"[show_mouse_press] {event.x()=}, {event.y()=}, {event.button()=}")

    def show_mouse_release(self, event):
        print(f"[show_mouse_release] {event.x()=}, {event.y()=}, {event.button()=}")

    def show_mouse_move(self, event):
        print(f"[show_mouse_move] {event.x()=}, {event.y()=}, {event.button()=}")

    def set_ui(self):
        self.main_window.videowidget.mousePressEvent = self.show_mouse_press
        # self.main_window.videowidget.mouseReleaseEvent = self.show_mouse_release
        # self.main_window.videowidget.mouseMoveEvent = self.show_mouse_move

        self.main_window.openBtn.clicked.connect(self.open_file)
        self.main_window.playBtn.clicked.connect(self.play_video)
        self.main_window.slider.sliderMoved.connect(self.set_position)

        self.main_window.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.main_window.mediaPlayer.positionChanged.connect(self.position_changed)
        self.main_window.mediaPlayer.durationChanged.connect(self.duration_changed)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.gray)
        self.setPalette(palette)

        self.UI_function = UI_function(self)
        self.init_ui()
        self.showFullScreen()

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

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(self.videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(self.videowidget)

        self.UI_function.set_ui()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
