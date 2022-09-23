from multiprocessing import set_forkserver_preload
from re import T
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2
import numpy as np
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh
from PyQt5.QtWidgets import QMessageBox

from UI6 import Ui_MainWindow

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.scene = QtWidgets.QGraphicsScene(self.ui.centralwidget)
        self.ui.graphicsView.setScene(self.scene)
        # self.img = QPixmap('1.jpg')         # 加入圖片
        # self.scene.addPixmap(self.img)                    # 將圖片加入 scene
        # self.ui.graphicsView.setScene(self.scene)                  # 設定 QGraphicsView 的場景為 scene
        self.step = 0
        self.img_hight = 0
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.horizontalSlider.setGraphicsEffect(self.op)
        self.ui.horizontalSlider.setEnabled(False)


        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.label_min.setGraphicsEffect(self.op)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.label_max.setGraphicsEffect(self.op)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.label_th.setGraphicsEffect(self.op)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.label_op.setGraphicsEffect(self.op)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
        self.ui.doubleSpinBox_min.setEnabled(False)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
        self.ui.doubleSpinBox_max.setEnabled(False)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
        self.ui.doubleSpinBox_th.setEnabled(False)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
        self.ui.doubleSpinBox_ol.setEnabled(False)

        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0)
        self.ui.btn_blob.setGraphicsEffect(self.op)
        self.ui.btn_blob.setEnabled(False)



    def setup_control(self):
        self.ui.fileButton.clicked.connect(self.open_file) 
        self.img_path = '1.jpg'
        self.ui.btn_zoom_in.clicked.connect(self.func_zoom_in) 
        self.ui.btn_zoom_out.clicked.connect(self.func_zoom_out)
        self.ui.btn_blob.clicked.connect(self.setting_btn_fn)
        # self.ui.scrollArea.setWidgetResizable(True)
        # self.ui.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # self.ui.label_img.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) # 將圖片置中
        # self.ui.graphicsView.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        # self.ui.graphicsView.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) # 將圖片置中
        self.ui.btn_next.clicked.connect(self.btn_next_fn) 
        self.ui.btn_prt.clicked.connect(self.btn_prt_fn) 
        self.ui.horizontalSlider.valueChanged.connect(self.getslidervalue)

    def setting_btn_fn(self):
        self.step == 3
        self.blob_img()

    def open_file(self):
        self.step = 1
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        if filename.split('.')[-1] not in ['jpg', 'bmp', 'png', 'jpeg', 'jfif']:
            QMessageBox.about(self, "ERROR", "請選擇圖片檔案")
            return 0

        if filename:
            self.ui.show_file_path.setText(filename)
            self.img_path = filename
            self.display_img()

    def getslidervalue(self):        
        # self.ui.label.setText(f"{self.ui.horizontalSlider.value()}")
        if self.step == 2:
            self.binarization()
        # if self.step == 3:
        #     self.binarization()
        #     self.blob_img()
        # print(self.ui.horizontalSlider.value())

    def display_img(self):
        self.ui.lab_bar.setText(f"")
        self.img = cv2.imread(self.img_path)
        height, width, channel = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.qpixmap_height = self.qpixmap.height()
        self.img_hight = self.qpixmap.height()
        # self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))
        # self.img = QPixmap(self.img_path)         # 加入圖片
        self.scene.clear()
        self.scene.addPixmap(self.qpixmap)                    # 將圖片加入 scene
        self.ui.graphicsView.setScene(self.scene)                  # 設定 QGraphicsView 的場景為 scene
        # self.ui.graphicsView.centerOn(self.scene)
        # self.ui.graphicsView.centerOn(self.ui.graphicsView.width()*0.5,self.ui.graphicsView.height()*0.5)
        # print(self.ui.graphicsView.width()*0.5,self.ui.graphicsView.height()*0.5)
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        # print(self.gray.shape)
        self.gray_three_channel = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
        # height, width, channel = self.gray_three_channel.shape
        # bytesPerline = 3 * width
        # self.qimg = QImage(self.gray_three_channel, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        # self.qpixmap = QPixmap.fromImage(self.qimg)
        # self.qpixmap_height = self.qpixmap.height()
        # self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))

    def func_zoom_in(self):
        self.ui.graphicsView.scale(0.8,0.8)   # Increase zoom

        # self.img_hight -= 100
        # self.qpixmap_height = self.img_hight
        # self.qpixmap_height -= 100
        self.update_img()

    def func_zoom_out(self):
        self.ui.graphicsView.scale(1.2,1.2)   # Increase zoom

        # self.img_hight += 100
        # self.qpixmap_height = self.img_hight
        # self.qpixmap_height += 100
        self.update_img()

    # def resize_image(self):
    #     scaled_pixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)
    #     self.ui.label.setPixmap(scaled_pixmap)

    def update_img(self):        
        self.qpixmap_height = self.img_hight
        scaled_pixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)
        # print(f"current img shape = ({scaled_pixmap.width()}, {scaled_pixmap.height()})")
        # self.ui.lab_bar.setText(f"({scaled_pixmap.width()} x {scaled_pixmap.height()})")
        # self.ui.label_img.setPixmap(scaled_pixmap)
        # self.ui.graphicsView.setPixmap(scaled_pixmap)
        self.scene.clear()
        self.scene.addPixmap(scaled_pixmap)                    # 將圖片加入 scene
        # self.ui.graphicsView.centerOn(self.ui.graphicsView.width()*0.5,self.ui.graphicsView.height()*0.5)
        # self.ui.graphicsView.mapToScene(self.ui.graphicsView.viewport().rect().center()) 
        self.ui.graphicsView.setScene(self.scene)                  # 設定 QGraphicsView 的場景為 scene

        # print(self.ui.graphicsView.width()*0.5,self.ui.graphicsView.height()*0.5)
        self.ui.btn_prt.setText("Previous")
        self.ui.btn_next.setText("Next")

    def btn_next_fn(self):
        if self.step >= 0 and self.step <= 3: 
            self.step += 1
            self.btn_status()

    def btn_prt_fn(self):
        if self.step >= 2 and self.step <= 4: 
            self.step -= 1
            self.btn_status()
        
    def btn_status(self):
        if self.step == 1:

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.horizontalSlider.setGraphicsEffect(self.op)
            self.ui.horizontalSlider.setEnabled(False)


            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_min.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_max.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_th.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_op.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_min.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_max.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_th.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_ol.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.btn_blob.setGraphicsEffect(self.op)
            self.ui.btn_blob.setEnabled(False)

            self.ui.lab_bar.setText(f"")
            self.img = cv2.imread(self.img_path)
            height, width, channel = self.img.shape
            bytesPerline = 3 * width
            self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
            self.qpixmap = QPixmap.fromImage(self.qimg)
            # self.qpixmap_height = self.qpixmap.height()
            # self.img_hight = self.qpixmap.height()
            self.qpixmap_height = self.img_hight
            self.update_img()
            self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            self.gray_three_channel = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
            # self.togary_fn()
            # self.binarization()
        elif self.step == 2:
            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.horizontalSlider.setGraphicsEffect(self.op)
            self.ui.horizontalSlider.setEnabled(True)


            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_min.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_max.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_th.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.label_op.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_min.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_max.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_th.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_ol.setEnabled(False)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.btn_blob.setGraphicsEffect(self.op)
            self.ui.btn_blob.setEnabled(False)

            self.binarization()
            # self.blob_img()
        elif self.step == 3:
            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.horizontalSlider.setGraphicsEffect(self.op)
            self.ui.horizontalSlider.setEnabled(False)


            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_min.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_max.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_th.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_op.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_min.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_max.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_th.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_ol.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.btn_blob.setGraphicsEffect(self.op)
            self.ui.btn_blob.setEnabled(True)

            # self.ui.label_max.setGraphicsEffect(self.op)
            # self.ui.label_th.setGraphicsEffect(self.op)
            # self.ui.label_op.setGraphicsEffect(self.op)
            # self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
            # self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
            # self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
            # self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
            # self.addtext()
            # self.ui.horizontalSlider.setHidden(True)
            # self.ui.label_min.setHidden(False)
            # self.ui.label_max.setHidden(False)
            # self.ui.label_th.setHidden(False)
            # self.ui.label_op.setHidden(False)
            # self.ui.doubleSpinBox_min.setHidden(False)
            # self.ui.doubleSpinBox_max.setHidden(False)
            # self.ui.doubleSpinBox_th.setHidden(False)
            # self.ui.doubleSpinBox_ol.setHidden(False)
            self.blob_img()

        elif self.step == 4:
            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(0)
            self.ui.horizontalSlider.setGraphicsEffect(self.op)
            self.ui.horizontalSlider.setEnabled(False)


            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_min.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_max.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_th.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.label_op.setGraphicsEffect(self.op)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_min.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_min.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_max.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_max.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_th.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_th.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.doubleSpinBox_ol.setGraphicsEffect(self.op)
            self.ui.doubleSpinBox_ol.setEnabled(True)

            self.op = QtWidgets.QGraphicsOpacityEffect()
            self.op.setOpacity(1)
            self.ui.btn_blob.setGraphicsEffect(self.op)
            self.ui.btn_blob.setEnabled(True)
            # self.ui.horizontalSlider.setHidden(True)
            # self.ui.label_min.setHidden(False)
            # self.ui.label_max.setHidden(False)
            # self.ui.label_th.setHidden(False)
            # self.ui.label_op.setHidden(False)
            # self.ui.doubleSpinBox_min.setHidden(False)
            # self.ui.doubleSpinBox_max.setHidden(False)
            # self.ui.doubleSpinBox_th.setHidden(False)
            # self.ui.doubleSpinBox_ol.setHidden(False)
            self.addtext()
        #     self.fin()

    # def togary_fn(self):
    #     self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
    #     # print(self.gray.shape)
    #     self.gray_three_channel = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
    #     height, width, channel = self.gray_three_channel.shape
    #     bytesPerline = 3 * width
    #     self.qimg = QImage(self.gray_three_channel, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    #     self.qpixmap = QPixmap.fromImage(self.qimg)
    #     self.qpixmap_height = self.qpixmap.height()
    #     self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))


    def binarization(self):
        self.ui.lab_bar.setText(f"Threshold :{self.ui.horizontalSlider.value()}")
        # print(self.ui.horizontalSlider.value())
        threshold = self.ui.horizontalSlider.value()
        self.cell_bw = self.gray.copy()
        self.cell_bw_three_channel = self.img.copy()
        thre,self.cell_bw = cv2.threshold(self.gray,threshold,255,cv2.THRESH_BINARY)#二值化
        # b, g, r = cv2.split(self.cell_bw_three_channel)
        # rgba = [b,g,r, self.cell_bw]
        # dst = cv2.merge(rgba,4)

        # cv2.cvtColor(dst, cv2.COLOR_BGRA2BGR)#透明層

        self.cell_bw_three_channel = cv2.cvtColor(self.cell_bw, cv2.COLOR_GRAY2BGR)

        self.cell_bw_three_channel = cv2.cvtColor(self.cell_bw_three_channel, cv2.COLOR_BGR2BGRA)#透明層
        # print(self.cell_bw_three_channel.shape)
        self.img_4 = cv2.cvtColor(self.img, cv2.COLOR_BGR2BGRA)#透明層
        # print(self.img_4.shape)
        alpha = 0.6
        self.cell_bw_three_channel = cv2.addWeighted(self.cell_bw_three_channel, alpha, self.img_4, 1 - alpha, 0)
        self.cell_bw_three_channel = cv2.cvtColor(self.cell_bw_three_channel, cv2.COLOR_BGRA2BGR)#透明層
        
        height, width, channel = self.cell_bw_three_channel.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.cell_bw_three_channel, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        # self.qpixmap_height = self.qpixmap.height()
        self.qpixmap_height = self.img_hight
        # print(self.img_hight)
        self.update_img()
        self.ui.btn_prt.setText("Previous")
        self.ui.btn_next.setText("Next")
        # self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))


    def blob_img(self):

        min_sigma = self.ui.doubleSpinBox_min.value()
        max_sigma = self.ui.doubleSpinBox_max.value()
        threshold = self.ui.doubleSpinBox_th.value()
        overlap = self.ui.doubleSpinBox_ol.value()

        # self.blobs_log = blob_log(self.cell_bw,min_sigma = 4, max_sigma=5.5, num_sigma=10, threshold=.0001,overlap=0.7)
        self.blobs_log = blob_log(self.cell_bw,min_sigma = min_sigma, max_sigma=max_sigma, num_sigma=10, threshold=threshold,overlap=overlap)

        # Compute radii in the 3rd column.
        self.blobs_log[:, 2] = self.blobs_log[:, 2] * sqrt(2)
        self.output1img=self.img.copy()
        for i in range(self.blobs_log.shape[0]):
            y, x, r = self.blobs_log [i,]
            # c = plt.Circle((x, y), r, color='r', linewidth=1, fill=False)
            cv2.circle(self.output1img,(int(x), int(y)), int(r), color=(0,0,255), thickness=2)
            # y=10 if x<10 else x #防止編號到圖片之外
            # ax.text(x, y, str(i))
            # ax.text(x,y, str(i), fontdict=font)
            cv2.putText(self.output1img,str(i), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1) #在左上角寫上編號
            # ax.add_patch(c)

        # # fig, ax = plt.subplots(figsize=(20, 20), sharex=True, sharey=True)
        # # cv2.imshow('output1img',self.output1img)
        # # cv2.waitKey(0)

        # height, width, channel = self.output1img.shape
        # bytesPerline = 3 * width
        # self.qimg = QImage(self.output1img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        # self.qpixmap = QPixmap.fromImage(self.qimg)
        # # self.qpixmap_height = self.qpixmap.height()
        # self.qpixmap_height = self.img_hight
        # # print(self.img_hight)
        # self.update_img()
        # print(self.blobs_log.shape [0])
        # # self.ui.lab_bar.setText(f"細胞數 :{self.blobs_log.shape [0]}")
        # # self.ui.label_img.setPixmap(QPixmap.fromImage(self.qimg))

    # def fin(self):
        self.gray_three_channel = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
        # ax.imshow(gray, interpolation='nearest',cmap="gray")
        shapes = np.zeros_like(self.gray_three_channel, np.uint8)

        for i in range(self.blobs_log.shape[0]):
            y, x, r = self.blobs_log [i,]
            # ax.text(x,y, str(i), fontdict=font)

            # # Draw shapes
            # cv2.rectangle(shapes, (5, 5), (100, 75), (255, 255, 255), cv2.FILLED)
            # cv2.circle(shapes, (300, 300), 75, (255, 255, 255), cv2.FILLED)

            # Generate output by blending image with shapes image, using the shapes
            # images also as mask to limit the blending to those parts
        

            if r > 0:
                # c = plt.Circle((x, y), r, color="red", alpha = 0.4, linewidth=2, fill=True)
                cv2.circle(shapes,(int(x), int(y)), int(r), color=(0,0,255), thickness=-1)

                # ax.add_patch(c)
            # else:
            #     # c = plt.Circle((x, y), r, color="cyan", linewidth=2, fill=False)
            #     cv2.circle(gray_three_channel,(int(x), int(y)), int(r), color=(0,0,255), thickness=-1)
            #     # ax.add_patch(c)
        self.out = self.gray_three_channel.copy()
        alpha = 0.2
        mask = shapes.astype(bool)
        self.out[mask] = cv2.addWeighted(self.gray_three_channel, alpha, shapes, 1 - alpha, 0)[mask]
        # cv2.imshow('out',out)
        # cv2.waitKey(0)
        height, width, channel = self.out.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.out, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        # self.qpixmap_height = self.qpixmap.height()
        self.qpixmap_height = self.img_hight
        # print(self.img_hight)
        self.update_img()
        print(self.blobs_log.shape [0])
        self.ui.lab_bar.setText(f"細胞數 :{self.blobs_log.shape [0]}")
        self.ui.btn_prt.setText("Previous")
        self.ui.btn_next.setText("顯示標號")

    def addtext(self):
        for i in range(self.blobs_log.shape[0]):
            y, x, r = self.blobs_log [i,]
            # c = plt.Circle((x, y), r, color='r', linewidth=1, fill=False)
            cv2.circle(self.out,(int(x), int(y)), int(r), color=(0,0,255), thickness=2)
            # y=10 if x<10 else x #防止編號到圖片之外
            # ax.text(x, y, str(i))
            # ax.text(x,y, str(i), fontdict=font)
            cv2.putText(self.out,str(i), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1) #在左上角寫上編號
            # ax.add_patch(c)
        height, width, channel = self.out.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.out, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.qpixmap_height = self.img_hight
        self.update_img()
        print(self.blobs_log.shape [0])
        self.ui.btn_prt.setText("隱藏標號")
        self.ui.btn_next.setText("顯示標號")