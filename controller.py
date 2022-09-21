from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2

from UI3 import Ui_MainWindow

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.fileButton.clicked.connect(self.open_file) 
        self.img_path = '1.jpg'
        self.ui.btn_zoom_in.clicked.connect(self.func_zoom_in) 
        self.ui.btn_zoom_out.clicked.connect(self.func_zoom_out)
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.label_img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) # 將圖片置中
        self.ui.submitButton.clicked.connect(self.subbtn) 


    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.ui.show_file_path.setText(filename)
        self.display_img()

    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.qpixmap_height = self.qpixmap.height()
        self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))

    def func_zoom_in(self):
        self.qpixmap_height -= 100
        self.img_resize()

    def func_zoom_out(self):
        self.qpixmap_height += 100
        self.img_resize()

    # def resize_image(self):
    #     scaled_pixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)
    #     self.ui.label.setPixmap(scaled_pixmap)

    def img_resize(self):        
        scaled_pixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)
        # print(f"current img shape = ({scaled_pixmap.width()}, {scaled_pixmap.height()})")
        self.ui.lab_bar.setText(f"({scaled_pixmap.width()} x {scaled_pixmap.height()})")
        self.ui.label_img.setPixmap(scaled_pixmap)

    def subbtn(self):
        # self.img = cv2.imread(self.img_path)
        
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        print(self.gray.shape)
        self.gray_three_channel = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
        height, width, channel = self.gray_three_channel.shape
        print(height, width, channel)

        bytesPerline = 3 * width
        self.qimg = QImage(self.gray_three_channel, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.qpixmap_height = self.qpixmap.height()
        self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))

    def aaa(self):
        threshold = 100  # 初始化threshold
        cell_bw = self.gray.copy()
        
        def threshold_fn(val):
            global gray,threshold,cell_bw
            threshold = val
            print(threshold)
        
            thre,cell_bw=cv2.threshold(gray,threshold,255,cv2.THRESH_BINARY)#二值化
            cell_bw_three_channel = cv2.cvtColor(cell_bw, cv2.COLOR_GRAY2BGR)
            # img_3 = np.concatenate((img,cell_bw_three_channel), axis=1)
            # cv2.imshow('threshold', img_3)
            # cv2.imshow('threshold', cell_bw)


        cv2.createTrackbar('threshold', 'threshold', 0, 255, threshold_fn)  # 加入亮度調整滑桿
        cv2.setTrackbarPos('threshold', 'threshold', 100)

        keycode = cv2.waitKey(0)
        cv2.destroyAllWindows()