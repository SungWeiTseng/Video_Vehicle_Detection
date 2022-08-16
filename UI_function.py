import cv2
from PIL import Image
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QAbstractVideoSurface, QVideoFrame, QAbstractVideoBuffer
from PyQt5.QtWidgets import QFileDialog, QStyle


class ReidUIFunction:
    def __init__(self, window):
        self.reidWindow = window

    def set_function(self):
        ...

    def paint_BBox(self):
        ...


class MainUIFunction:
    def __init__(self, main_window):
        self.mainWindow = main_window
        self.mousePos = None
        self.selectedImage = None

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open Video")

        if filename != '':
            self.mainWindow.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.mainWindow.playBtn.setEnabled(True)

    def play_video(self):
        if self.mainWindow.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mainWindow.mediaPlayer.pause()
        else:
            self.mainWindow.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mainWindow.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mainWindow.playBtn.setIcon(
                self.mainWindow.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.mainWindow.playBtn.setIcon(
                self.mainWindow.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.mainWindow.slider.setValue(position)

    def duration_changed(self, duration):
        self.mainWindow.slider.setRange(0, duration)

    def set_position(self, position):
        self.mainWindow.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.mainWindow.playBtn.setEnabled(False)
        self.mainWindow.label.setText("Error: " + self.mainWindow.mediaPlayer.errorString())

    def on_mouse_press(self, event):
        # self.main_window.label.setText(f"[show_mouse_press] {event.x()}, {event.y()}, {event.button()}")
        if event.button() == 1:
            self.mousePos = (event.x(), event.y())
            self.mainWindow.reidWindow.show()
            if self.check_BBox():
                result = self.ReID_inference()
        # print(f"[show_mouse_press] {event.x()}, {event.y()}, {event.button()}")

    def show_mouse_release(self, event):
        print(f"[show_mouse_release] {event.x()}, {event.y()}, {event.button()}")

    def show_mouse_move(self, event):
        print(f"[show_mouse_move] {event.x()}, {event.y()}, {event.button()}")

    def process_frame(self, image):
        self.mainWindow.imgLabel.setPixmap(QPixmap.fromImage(image))

    def check_BBox(self) -> bool:
        return False

    def ReID_inference(self):
        return None

    def set_function(self):

        self.mainWindow.grabber.frameAvailable.connect(self.process_frame)
        self.mainWindow.imgLabel.mousePressEvent = self.on_mouse_press
        # self.main_window.videowidget.mouseReleaseEvent = self.show_mouse_release
        # self.main_window.videowidget.mouseMoveEvent = self.show_mouse_move

        self.mainWindow.openBtn.clicked.connect(self.open_file)
        self.mainWindow.playBtn.clicked.connect(self.play_video)
        self.mainWindow.slider.sliderMoved.connect(self.set_position)

        self.mainWindow.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mainWindow.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mainWindow.mediaPlayer.durationChanged.connect(self.duration_changed)


class VideoFrameGrabber(QAbstractVideoSurface):
    frameAvailable = pyqtSignal(QImage)

    def __init__(self, parent):
        super().__init__(parent)

    def supportedPixelFormats(self, handleType):
        return [QVideoFrame.Format_ARGB32, QVideoFrame.Format_ARGB32_Premultiplied,
                QVideoFrame.Format_RGB32, QVideoFrame.Format_RGB24, QVideoFrame.Format_RGB565,
                QVideoFrame.Format_RGB555, QVideoFrame.Format_ARGB8565_Premultiplied,
                QVideoFrame.Format_BGRA32, QVideoFrame.Format_BGRA32_Premultiplied, QVideoFrame.Format_BGR32,
                QVideoFrame.Format_BGR24, QVideoFrame.Format_BGR565, QVideoFrame.Format_BGR555,
                QVideoFrame.Format_BGRA5658_Premultiplied, QVideoFrame.Format_AYUV444,
                QVideoFrame.Format_AYUV444_Premultiplied, QVideoFrame.Format_YUV444,
                QVideoFrame.Format_YUV420P, QVideoFrame.Format_YV12, QVideoFrame.Format_UYVY,
                QVideoFrame.Format_YUYV, QVideoFrame.Format_NV12, QVideoFrame.Format_NV21,
                QVideoFrame.Format_IMC1, QVideoFrame.Format_IMC2, QVideoFrame.Format_IMC3,
                QVideoFrame.Format_IMC4, QVideoFrame.Format_Y8, QVideoFrame.Format_Y16,
                QVideoFrame.Format_Jpeg, QVideoFrame.Format_CameraRaw, QVideoFrame.Format_AdobeDng]

    def present(self, frame):
        if frame.isValid():
            cloneFrame = QVideoFrame(frame)
            cloneFrame.map(QAbstractVideoBuffer.ReadOnly)
            image = QImage(cloneFrame.bits(), cloneFrame.width(), cloneFrame.height(),
                           QVideoFrame.imageFormatFromPixelFormat(cloneFrame.pixelFormat()))
            self.frameAvailable.emit(image)  # this is very important
            cloneFrame.unmap()
        # return True
        return False
