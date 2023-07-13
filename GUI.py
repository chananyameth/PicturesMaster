import sys
import subprocess
import random
import os
import time
from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtSql import QSqlDatabase, QSqlQuery


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
        labels['Source'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Destination'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Source'] = QLineEdit()
        self.lineEdits['Destination'] = QLineEdit()

        layout.addWidget(labels['Source'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Source'],    0, 1, 1, 3)

        layout.addWidget(labels['Destination'],            1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Destination'],    1, 1, 1, 3)

        button_login = QPushButton('&Log In', clicked=self.check_credential)
        layout.addWidget(button_login,                  2, 3, 1, 1)

        self.status = QLabel('put here the status')
        self.status.setStyleSheet('font-size: 15px; color: red; background: yellow')
        layout.addWidget(self.status, 3, 0, 1, 4)


        button1 = QPushButton("Copy from phone")
        button2 = QPushButton("Standardize files' names")
        button3 = QPushButton("Flat folder to tree")
        button4 = QPushButton("Click me! get directory", clicked=self.get_directory_path)

        layout.addWidget(button1, 4, 0)
        layout.addWidget(button2, 4, 1)
        layout.addWidget(button3, 4, 2)
        layout.addWidget(button4, 5, 0, 1, 1)
        layout.addWidget(QPushButton("Choose", clicked=lambda: self.get_directory_path("Source")), 0, 4, 1, 1)
        layout.addWidget(QPushButton("Choose", clicked=lambda: self.get_directory_path("Destination")), 1, 4, 1, 1)

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

    def check_credential(self):
        username = self.lineEdits['Source'].text()
        password = self.lineEdits['Destination'].text()
        print(username, password)

        # commands = ["ls /storage/emulated/0/DCIM/Camera\n", "pwd"]
        commands = [username + '\n']
        output = subprocess.check_output([r"C:\Users\Chananya\Downloads\adb\adb.exe", "shell", *commands])
        for line in output.split(b'\r\n'):
            print(line.decode("utf-8"))

    #     self.button.clicked.connect(self.magic)
    #
    # @QtCore.Slot()
    # def magic(self):
    #     self.text.setText(random.choice(self.hello))

    @property
    def source_path(self):
        return self.lineEdits['Source'].text()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainApp()
    widget.show()
    sys.exit(app.exec())
