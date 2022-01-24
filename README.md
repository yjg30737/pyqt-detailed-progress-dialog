# pyqt-detailed-progress-dialog
PyQt Detailed Progress Dialog (Show the download/copy&paste progress in detail with QListWidget like adding the filename on QListWidget right after it was pasted)

## Requirements
* PyQt5 >= 5.15

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-detailed-progress-dialog.git --upgrade```

## Description
This dialog's UI mainly consists of <b>QProgressBar</b>, <b>QListWidget</b>. QProgressBar shows how much an operation is being progressed, QListWidget shows the pasted filename like installed files list. QListWidget can be hidden by clicking the show/hide detail toggle button. 

Main operation of this dialog is <b>copy and paste</b> the files. You can give filenames which you want to copy to constructor. Then ```ProgressWorkingThread(QThread)``` which is connected with dialog will do the copy and paste operation.

## Usage
* ```canceled``` signal is emitted when the cancel button is clicked. This is connected to the close() method by default.
* ```completed``` signal is emitted when operation is finished.
* Main class is DetailedProgressDialog. Constructor's format is ```DetailedProgressDialog(filenames: list)```.

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
        path_lst = []
        for path, dir, files in os.walk(pathname):
            for filename in files:
                path_filename = os.path.join(path, filename)
                path_lst.append(path_filename)
        return path_lst

    def __download(self):
        filenames = self.getAllFilesInPath(os.path.join(os.path.dirname(__file__), 'src')) # Get all the filenames list in certain directory
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





