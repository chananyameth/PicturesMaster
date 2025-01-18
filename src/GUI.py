import logging
import subprocess
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, \
    QSizePolicy

from src.copy_from_phone import copy_from_phone
from src.status_history import StatusHistory

logging.basicConfig(level=logging.NOTSET)


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pictures Master')
        self.setWindowIcon(QIcon(''))
        self.resize(800, 600)

        layout = QGridLayout()
        self.setLayout(layout)

        self.paths = {}
        labels = {}
        self.lineEdits = {}

        labels['Source'] = QLabel('Source')
        labels['Destination'] = QLabel('Destination')
        labels['Command'] = QLabel('ADB Command')
        labels['Source'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Destination'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Source'] = QLineEdit()
        self.lineEdits['Destination'] = QLineEdit()
        self.lineEdits['Command'] = QLineEdit()

        layout.addWidget(labels['Source'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Source'],    0, 1, 1, 3)

        layout.addWidget(labels['Destination'],            1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Destination'],    1, 1, 1, 3)

        layout.addWidget(labels['Command'],            2, 0, 1, 1)
        layout.addWidget(self.lineEdits['Command'],    2, 1, 1, 3)
        button_run_command = QPushButton('&Run Command', clicked=self.run_command)
        layout.addWidget(button_run_command,                  2, 4, 1, 1)

        self.status = QLabel('put here the status')
        self.status.setStyleSheet('font-size: 15px; color: red; background: yellow')
        StatusHistory.add_on_update_handler_full_history(self.status.setText)
        layout.addWidget(self.status, 3, 0, 1, 4)

        button1 = QPushButton("Copy from phone", clicked=copy_from_phone)
        button2 = QPushButton("Standardize files' names")
        button3 = QPushButton("Flat folder to tree")
        button4 = QPushButton("Click me! get directory", clicked=self.get_directory_path)

        layout.addWidget(button1, 4, 0)
        layout.addWidget(button2, 4, 1)
        layout.addWidget(button3, 4, 2)
        layout.addWidget(button4, 5, 0, 1, 1)
        layout.addWidget(QPushButton("Choose source dir", clicked=lambda: self.get_directory_path("Source")), 0, 4, 1, 1)
        layout.addWidget(QPushButton("Choose destination dir", clicked=lambda: self.get_directory_path("Destination")), 1, 4, 1, 1)


    def get_directory_path(self, var_name='dir_path'):
        dlg = QFileDialog(self, Qt.WindowType.Dialog)
        dlg.setFileMode(QFileDialog.Directory)

        try:
            dlg.fileSelected.connect(self.lineEdits[var_name].setText)
        except Exception:
            pass

        if dlg.exec():
            self.paths[var_name] = dlg.selectedFiles()[0]
            print(self.paths[var_name])
            self.status.setText("directory path: " + self.paths[var_name])
        else:
            self.status.setText("Can't get directory from dialog")

    def run_command(self):
        # commands = ["ls /storage/emulated/0/DCIM/Camera | wc -l\n", "pwd"]
        command = self.lineEdits['Command'].text()
        commands = [command + '\n']
        output = subprocess.check_output([r"C:\Chananya\Software\adb\adb.exe", "shell", *commands])
        for line in output.split(b'\r\n'):
            print(line.decode("utf-8"))

    @property
    def source_path(self):
        return self.lineEdits['Source'].text()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainApp()
    widget.show()
    sys.exit(app.exec())
