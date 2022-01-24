from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QFrame, QListWidget, \
    QProgressBar
from PyQt5.QtCore import Qt, pyqtSignal

from pyqt_detailed_progress_dialog.progressWorkingThread import ProgressWorkingThread


class DetailedProgressDialog(QDialog):
    canceled = pyqtSignal()
    completed = pyqtSignal()

    def __init__(self, filenames: list):
        super().__init__()
        self.__filenames = filenames
        self.__min = 0
        self.__max = len(self.__filenames)
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Downloading...')
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.__progressBar = QProgressBar()
        self.__progressBar.setRange(self.__min, self.__max)

        lay = QVBoxLayout()
        lay.addWidget(self.__progressBar)
        lay.setContentsMargins(0, 2, 0, 2)
        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__showInDetailBtn = QPushButton('Show Detail')
        self.__showInDetailBtn.setCheckable(True)
        self.__showInDetailBtn.toggled.connect(self.__showInDetail)

        lay = QHBoxLayout()
        lay.addWidget(self.__showInDetailBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomLeftWidget = QWidget()
        bottomLeftWidget.setLayout(lay)

        cancelBtn = QPushButton('Cancel')
        cancelBtn.clicked.connect(self.close)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignRight)
        lay.addWidget(cancelBtn)
        lay.setContentsMargins(0, 0, 0, 0)
        bottomRightWidget = QWidget()
        bottomRightWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(bottomLeftWidget)
        lay.addWidget(bottomRightWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        self.__detailWidget = QListWidget()
        self.__detailWidget.setVisible(False)

        self.__showInDetailBtn.toggle()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(self.__detailWidget)
        lay.addWidget(line)
        lay.addWidget(bottomWidget)
        self.setLayout(lay)

        self.perform()

    def __showInDetail(self, f):
        if f:
            self.__showInDetailBtn.setText('Hide')
        else:
            self.__showInDetailBtn.setText('Show Detail')
        self.__detailWidget.setVisible(f)
        self.adjustSize()

    def __addItemToDetailWidget(self, item):
        self.__detailWidget.addItem(item)
        self.__detailWidget.scrollToBottom()

    def perform(self):
        self.__thread = ProgressWorkingThread(self.__filenames)
        self.__thread.updateCount.connect(self.__progressBar.setValue)
        self.__thread.updatePastedFile.connect(self.__addItemToDetailWidget)
        self.__thread.start()
        self.__thread.finished.connect(self.complete)

    def complete(self):
        self.completed.emit()

    def closeEvent(self, e):
        self.canceled.emit()
        return super().closeEvent(e)
