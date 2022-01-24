# pyqt-detailed-progress-dialog
PyQt Detailed Progress Dialog (Show the download/copy&paste progress in detail with QListWidget like adding the filename on QListWidget right after it was pasted)

## Requirements
* PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-detailed-progress-dialog.git --upgrade```

## Example
Code Sample
```python
import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from pyqt_detailed_progress_dialog import DetailedProgressDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        downloadStartBtn = QPushButton('Start the download')
        downloadStartBtn.clicked.connect(self.__download)
        self.setCentralWidget(downloadStartBtn)

    def getAllFilesInPath(self, pathname):
        rel_path_lst = []
        for path, dir, files in os.walk(pathname):
            for filename in files:
                rel_path = os.path.join(path, filename)
                rel_path_lst.append(rel_path)
        return rel_path_lst

    def __download(self):
        filenames = self.getAllFilesInPath(os.path.join(os.path.dirname(__file__), 'src'))
        self.__dialog = DetailedProgressDialog(filenames)
        self.__dialog.canceled.connect(self.cancel)
        self.__dialog.completed.connect(self.complete)
        self.__dialog.show()

    def cancel(self):
        print('cancel')

    def complete(self):
        print('complete')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```

Result

https://user-images.githubusercontent.com/55078043/150727857-2efcf017-82e9-4292-948d-ab45047b1c8d.mp4





