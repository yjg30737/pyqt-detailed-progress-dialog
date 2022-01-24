import shutil, os

from PyQt5.QtCore import QThread, pyqtSignal


class ProgressWorkingThread(QThread):
    updateCount = pyqtSignal(int)
    updatePastedFile = pyqtSignal(str)

    def __init__(self, filenames: list):
        super().__init__()
        self.__filenames = filenames

    def run(self):
        for i in range(len(self.__filenames)):
            filename = self.__filenames[i]
            shutil.copy(filename, 'dst')
            self.updateCount.emit(i+1)
            self.updatePastedFile.emit(os.path.basename(filename))
