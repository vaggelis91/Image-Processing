from PIL import Image, ImageFilter
from PyQt4 import QtGui, QtCore
import sys
import os


class subwindow(QtGui.QWidget):
    def __init__(self, name, default_width, default_height, parent=None):
        super(subwindow, self).__init__()
        Window.name = name
        Window.width = default_width
        Window.height = default_height
        self.file_name, self.file_ext = Window.name.split(".", 1)

        # STYLE SUB WINDOW
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(329, 215)
        self.setWindowTitle('Export Image')
        self.setWindowIcon(QtGui.QIcon('exporticon.png'))

        # LABELS
        imgSize = QtGui.QLabel('Image Size', self)
        imgSize.move(15, 10)
        imgWidth = QtGui.QLabel('Set Width:', self)
        imgWidth.move(75, 30)
        imgHeight = QtGui.QLabel('Set Height:', self)
        imgHeight.move(197, 30)
        imgType = QtGui.QLabel('Image Format', self)
        imgType.move(15, 70)
        imgType = QtGui.QLabel('Select Format:', self)
        imgType.move(75, 90)
        imgtip = QtGui.QLabel('Tip: Images can only become smaller based on width or height.', self)
        imgtip.move(15, 135)

        # TEXT BOXES COMBO BOX BUTTONS
        self.widthTextbox = QtGui.QLineEdit(self)
        self.widthTextbox.setText(str(Window.width))
        self.widthTextbox.setFixedWidth(50)
        self.widthTextbox.move(130, 27)

        self.heightTextbox = QtGui.QLineEdit(self)
        self.heightTextbox.setText(str(Window.height))
        self.heightTextbox.setFixedWidth(50)
        self.heightTextbox.move(255, 27)

        self.formatCombobox = QtGui.QComboBox(self)
        self.formatCombobox.addItems(["jpg", "png"])
        self.formatCombobox.setFixedWidth(60)
        self.formatCombobox.move(149, 87)

        exportButton = QtGui.QPushButton("&Export", self)
        exportButton.setFixedWidth(60)
        exportButton.move(190, 170)

        cancelButton = QtGui.QPushButton("Cancel", self)
        cancelButton.setFixedWidth(60)
        cancelButton.move(255, 170)

        if self.file_ext == 'png':
            self.widthTextbox.setEnabled(False)
            self.heightTextbox.setEnabled(False)

        # ACTIONS
        exportButton.clicked.connect(self.export_click)
        cancelButton.clicked.connect(self.cancel_click)
        self.formatCombobox.activated.connect(self.format_selection)

    def export_click(self):
        size_tuple = (int(self.widthTextbox.text()), int(self.heightTextbox.text()))
        export_image = Image.open(Window.name)
        export_file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', 'File Format (*.' + self.format_selection() + ')')
        try:
            if self.file_ext == 'png' and self.format_selection() == 'jpg':
                # CONVERT FROM .PNG TO .JPG
                my_palette = export_image.getpalette()
                export_image.putpalette(my_palette)
                bg = Image.new('RGBA', export_image.size)
                bg.paste(export_image)
                bg.save(export_file_name)
            else:
                export_image.thumbnail(size_tuple)
                export_image.save(export_file_name)
        except KeyError:
            pass

    def cancel_click(self):
        self.close()

    def format_selection(self):
        selected_format = self.formatCombobox.currentText()
        return selected_format


class Window(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.setGeometry(200, 100, 900, 600)
        self.setWindowTitle('Image Processor')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # FILE MENU ACTIONS
        openAction = QtGui.QAction("Open", self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.open_img)

        self.saveAsAction = QtGui.QAction("Save As", self)
        self.saveAsAction.setShortcut('Ctrl+A')
        self.saveAsAction.triggered.connect(self.saveAs_img)

        self.exportAction = QtGui.QAction("Export Image As", self)
        self.exportAction.setShortcut('Ctrl+E')
        self.exportAction.triggered.connect(self.export_img)

        histAction = QtGui.QAction("History", self)
        histAction.triggered.connect(self.history)

        exitAction = QtGui.QAction("Exit", self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close_application)

        # EDIT MENU ACTIONS
        self.blurAction = QtGui.QAction("Blur", self)
        self.blurAction.triggered.connect(self.blur_image)

        self.gaussianBlurAction = QtGui.QAction("Gaussian Blur", self)
        self.gaussianBlurAction.triggered.connect(self.gaussianBlur_image)

        self.contourAction = QtGui.QAction("Contour", self)
        self.contourAction.triggered.connect(self.contour_image)

        self.edgeEnAction = QtGui.QAction("Edge Enhance", self)
        self.edgeEnAction.triggered.connect(self.edgeEn_image)

        self.edgeEnMAction = QtGui.QAction("Edge Enhance More", self)
        self.edgeEnMAction.triggered.connect(self.edgeEnM_image)

        self.embossAction = QtGui.QAction("Emboss", self)
        self.embossAction.triggered.connect(self.emboss_image)

        self.maxfltAction = QtGui.QAction("Max Filter", self)
        self.maxfltAction.triggered.connect(self.maxflt_image)

        self.medianfltAction = QtGui.QAction("Median Filter", self)
        self.medianfltAction.triggered.connect(self.medianflt_image)

        self.minfltAction = QtGui.QAction("Min Filter", self)
        self.minfltAction.triggered.connect(self.minflt_image)

        self.findEdgesAction = QtGui.QAction("Find Edges", self)
        self.findEdgesAction.triggered.connect(self.findEdges_image)

        self.maskAction = QtGui.QAction("Unsharp Mask", self)
        self.maskAction.triggered.connect(self.mask_image)

        self.smoothAction = QtGui.QAction("Smooth", self)
        self.smoothAction.triggered.connect(self.smooth_image)

        self.smoothMAction = QtGui.QAction("Smooth More", self)
        self.smoothMAction.triggered.connect(self.smoothM_image)

        self.modeAction = QtGui.QAction("Mode Filter", self)
        self.modeAction.triggered.connect(self.mode_image)

        self.rankAction = QtGui.QAction("Rank Filter", self)
        self.rankAction.triggered.connect(self.rank_image)

        self.sharpenAction = QtGui.QAction("Sharpen", self)
        self.sharpenAction.triggered.connect(self.sharpen_image)

        self.detailAction = QtGui.QAction("Detail", self)
        self.detailAction.triggered.connect(self.detail_image)

        #MENU BAR
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.exportAction)
        self.addHistory = fileMenu.addMenu('History')
        fileMenu.addAction(exitAction)

        editMenu = mainMenu.addMenu('Edit')
        editMenu.addAction(self.blurAction)
        editMenu.addAction(self.contourAction)
        editMenu.addAction(self.detailAction)
        editMenu.addAction(self.sharpenAction)
        editMenu.addAction(self.edgeEnAction)
        editMenu.addAction(self.edgeEnMAction)
        editMenu.addAction(self.embossAction)
        editMenu.addAction(self.findEdgesAction)
        editMenu.addAction(self.gaussianBlurAction)
        editMenu.addAction(self.maskAction)
        editMenu.addAction(self.maxfltAction)
        editMenu.addAction(self.medianfltAction)
        editMenu.addAction(self.minfltAction)
        editMenu.addAction(self.modeAction)
        editMenu.addAction(self.rankAction)
        editMenu.addAction(self.smoothAction)
        editMenu.addAction(self.smoothMAction)
        editMenu.addAction(self.sharpenAction)

        self.set_to_false()

    def open_img(self):
        try:
            self.open_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', 'Image files (*.jpg *.png)')
            imgSize = Image.open(self.open_filename)
            self.width, self.height = imgSize.size
            # LOAD PICTURE
            win = QtGui.QWidget(self)
            lb1 = QtGui.QLabel()
            lb1.setAlignment(QtCore.Qt.AlignCenter)
            lb1.setPixmap(QtGui.QPixmap(self.open_filename))
            self.setCentralWidget(win)
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(lb1)
            win.setLayout(vbox)
            win.show()

            head, tail = os.path.split(self.open_filename)
            self.addHistory.addAction(tail)
            self.set_to_true()
        except:
            self.info_msg('Image file cannot be identified.')

    def saveAs_img(self):
        try:
            save_filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 'C:\\', "Image files (*.jpg *.png)")
            processed_img.save(save_filename)
        except NameError:
            self.info_msg('The image has not been processed yet.')

    def export_img(self):
        self.export_subwindow = subwindow(self.open_filename, self.width, self.height)
        self.export_subwindow.show()

    def history(self):
        pass

    def close_application(self):
        reply = QtGui.QMessageBox.question(self, 'Message', 'Exit Image Processing?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    # OPEN PROCESSED IMAGES
    def blur_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.BLUR)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def gaussianBlur_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.GaussianBlur)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def contour_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.CONTOUR)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def edgeEn_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.EDGE_ENHANCE)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def edgeEnM_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def emboss_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.EMBOSS)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def maxflt_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.MaxFilter)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def medianflt_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.MedianFilter)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def minflt_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.MinFilter)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def findEdges_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.FIND_EDGES)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def mask_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.UnsharpMask)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def smooth_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.SMOOTH)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def smoothM_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.SMOOTH_MORE)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def mode_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.ModeFilter)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def rank_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.RankFilter)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def sharpen_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.SHARPEN)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')

    def detail_image(self):
        try:
            global processed_img
            processed_img = Image.open(self.open_filename)
            processed_img = processed_img.filter(ImageFilter.DETAIL)
            processed_img.show()
        except ValueError:
            self.info_msg('Image cannot be processed. To process a .png image first export it to jpg.')


    def info_msg(self, message_text):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(message_text)
        msg.setWindowTitle("Message")
        msg.setWindowIcon(QtGui.QIcon("info.png"))
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()


    def set_to_false(self):
        self.saveAsAction.setEnabled(False)
        self.exportAction.setEnabled(False)
        self.blurAction.setEnabled(False)
        self.contourAction.setEnabled(False)
        self.detailAction.setEnabled(False)
        self.edgeEnAction.setEnabled(False)
        self.edgeEnMAction.setEnabled(False)
        self.embossAction.setEnabled(False)
        self.findEdgesAction.setEnabled(False)
        self.gaussianBlurAction.setEnabled(False)
        self.maskAction.setEnabled(False)
        self.maxfltAction.setEnabled(False)
        self.minfltAction.setEnabled(False)
        self.medianfltAction.setEnabled(False)
        self.modeAction.setEnabled(False)
        self.rankAction.setEnabled(False)
        self.smoothAction.setEnabled(False)
        self.smoothMAction.setEnabled(False)
        self.sharpenAction.setEnabled(False)


    def set_to_true(self):
        self.saveAsAction.setEnabled(True)
        self.exportAction.setEnabled(True)
        self.blurAction.setEnabled(True)
        self.contourAction.setEnabled(True)
        self.detailAction.setEnabled(True)
        self.edgeEnAction.setEnabled(True)
        self.edgeEnMAction.setEnabled(True)
        self.embossAction.setEnabled(True)
        self.findEdgesAction.setEnabled(True)
        self.gaussianBlurAction.setEnabled(True)
        self.maskAction.setEnabled(True)
        self.maxfltAction.setEnabled(True)
        self.minfltAction.setEnabled(True)
        self.medianfltAction.setEnabled(True)
        self.modeAction.setEnabled(True)
        self.rankAction.setEnabled(True)
        self.smoothAction.setEnabled(True)
        self.smoothMAction.setEnabled(True)
        self.sharpenAction.setEnabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()