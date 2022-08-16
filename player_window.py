import cv2
from PIL import Image, ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QImage, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, \
    QStyle

from UI_function import MainUIFunction, VideoFrameGrabber


'''
class GalleryBlock:
    def __init__(self, window):
        self.galleryImg = QLabel(window)
        self.imgPath = QLabel(window)
        self.distance = QLabel(window)

        # self.setUI()
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(0, 0, 0, 0)

    def setUI(self, image, path, distance):
        pixcelMap = QPixmap.fromImage(image).scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.galleryImg.setPixmap(pixcelMap)
        self.imgPath.setText(path)
        self.distance.setText(str(distance))
        self.vboxLayout.addWidget(self.imgPath)
        self.vboxLayout.addWidget(self.galleryImg)
        self.vboxLayout.addWidget(self.distance)
'''


class ReidWindow(QWidget):
    def __init__(self, mainWindow, numResult):
        super(ReidWindow, self).__init__()
        self.numRow = 5

        self.numResult = numResult
        self.setWindowTitle("Vehicle ReID Result")
        self.setGeometry(350, 100, 750, 500)

        # palette = self.palette()
        # palette.setColor(QPalette.Window, Qt.black)
        # self.setPalette(palette)

        self.mainWindow = mainWindow

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setContentsMargins(20, 20, 20, 20)
        self.hboxLayout = [QHBoxLayout() for _ in range(self.numResult // self.numRow)]
        self.galleryImg = [QLabel() for _ in range(self.numResult)]

    def get_text_image(self, gallery_path, distance):
        im = cv2.imread(gallery_path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = cv2.resize(im, (250, 250))
        cv2.putText(im, gallery_path.split('/')[-1], (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 128, 0), 1)
        cv2.putText(im, distance, (130, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        img = Image.fromarray(im).convert("RGBA")
        # data = im.tobytes("RGBA")
        # qim = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        # img.show()
        return ImageQt.ImageQt(img)

    def init_ui(self, resultList):

        self.resultList = resultList[:self.numResult]
        for col in range(self.numResult // self.numRow):
            self.hboxLayout[col].setContentsMargins(0, 0, 0, 0)
            for i in range(self.numRow):
                idx = col * self.numRow + i
                path = self.resultList[idx]["path"]
                dis = self.resultList[idx]["distance"]

                qtImage = self.get_text_image(path, dis)
                self.galleryImg[idx].setPixmap(QPixmap.fromImage(qtImage))
                # pixcelMap = QPixmap.fromImage(image).scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)

                self.hboxLayout[col].addWidget(self.galleryImg[idx])
            self.vboxLayout.addLayout(self.hboxLayout[col])
        self.setLayout(self.vboxLayout)


class mainWindow(QWidget):
    def __init__(self):
        super(mainWindow, self).__init__()

        self.numResult = 10

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)

        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.gray)
        self.setPalette(palette)

        self.reidWindow = ReidWindow(self, self.numResult)
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

        d = "10"
        n = ".jpg"
        img = "C:/Users/Admin/Desktop/005FzdTdgy1gegf7mm8qdj31hc0u07d6.jpg"
        result = [{"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d},
                  {"image": img, "path": img, "distance": d}]

        # img = self.resultList[idx]["image"]
        # path = self.resultList[idx]["path"]
        # dis = self.resultList[idx]["distance"]

        self.reidWindow.init_ui(result)
