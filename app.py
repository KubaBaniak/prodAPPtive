from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
import random
from datetime import datetime
from os import access, R_OK
from pathlib import Path
import sys


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProdAPPtive")
        self.setContentsMargins(40, 30, 40, 30)
        self.setFixedSize(600, 600)
        self.resize(600, 600)

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        stylesheet = """
            QWidget {
                background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #414141, stop: 1 #353535);
                font: cascasia code;
                color: #f0f7f4;
                margin: 5px;
            }

            QLabel {
                font-size: 18px;
                padding: 0 5px 0 5px;
                background-color: transparent;
            }

            QLabel#header{
                font-size: 28px;
                font-weight: bold;
            }
            

            QPushButton{
                border-style: solid;
                border-width: 2px;
                border-radius: 10px;
                border-color: #7e8d85;
                background-color: #4a4a47;
                font: bold 20px;
                max-width: 250px;
                height:35px;
            }

            QPushButton:hover{
                background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #b3bfb8, stop: 1 #a2e3c4);
                color: #32322C;
                font-size: 22px;
            }

            QPushButton:pressed {
                border-style: inset;
            }
        """
        self.setStyleSheet(stylesheet)

        widgets = self.create_widgets()

        [vbox.addWidget(widget) for widget in widgets]

    def create_widgets(self):
        self.intro_label = QLabel("Welcome to ProdAPPtive", self)
        self.search_button = QPushButton("Search File", self)
        self.file_name_label = QLabel("", self)
        self.block_button = QPushButton("Block File", self)
        self.unblock_button = QPushButton("Unblock File", self)
        self.info_label = QLabel("", self)
        self.recovery_button = QPushButton("Recovery mode", self)

        self.intro_label.setObjectName('header')
        self.intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_name_label.setWordWrap(True)
        self.info_label.setWordWrap(True)

        [widget.adjustSize() for widget in [self.file_name_label, self.info_label]]

        self.search_button.clicked.connect(self.search_file)
        self.block_button.clicked.connect(self.block_file)
        self.unblock_button.clicked.connect(self.unblock_file)
        self.recovery_button.clicked.connect(self.recover)

        return [self.intro_label, self.search_button, self.file_name_label, self.block_button, self.unblock_button, self.info_label, self.recovery_button]

    def search_file(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)")
        if self.fname:
            self.file_name_label.setText(self.fname)

    def self_file_validation(self):
        if (self.fname == __file__):
            self.info_label.setText("You cannot interact with this file")
            return True

    def block_file(self):

        if self.self_file_validation():
            return None

        if not Path("rescue_key.txt").is_file():
            with open('rescue_key.txt', 'w') as key_file:
                key = str(random.randint(1, 255))
                key_file.write(key)
                with open('recovery_file.txt', 'a') as recovery_file:
                    recovery_file.write(f'{datetime.now()}|{key}\n')

        def encrypt(filename):
            #reading the key to encrypt
            with open("rescue_key.txt", 'r') as f:
                key = int(f.read())
            #reading data
            with open(filename, 'rb') as f:
                data = f.read()
            data = bytearray(data)
            #encrypting data using XOR operation
            for index, value in enumerate(data):
                data[index] = value ^ key
            #writing encrypted data to file
            with open(filename, 'wb') as f:
                f.write(data)

            self.info_label.setText("File encrypted successfully, you can focus on your tasks")

        encrypt(self.fname)

    def unblock_file(self):

        def decrypt(filename):
            if self.self_file_validation():
                return None

            if not Path("rescue_key.txt").is_file():
                self.info_label.setText("Sir, we gotta problem... I cant find a key to unlock the file")
            else:
                with open("rescue_key.txt", 'r') as key_file:
                    key = int(key_file.read())
                with open(filename, 'rb') as f:
                    data = f.read()
                data = bytearray(data)
                #decrypting data using XOR operation
                for index, value in enumerate(data):
                    data[index] = value ^ key
                #writing decrypted data
                with open(filename, 'wb') as f:
                    f.write(data)
                self.info_label.setText("File decrypted Sir, go play and have some fun")
                
        decrypt(self.fname)
    
    def recover(self):
        with open('recovery_file.txt', 'r') as recovery_file:
            keys = recovery_file.read()
        keys = [key.split('|')[1] for key in keys.split('\n')[:-1]]
        print(keys)
        with open(self.fname, 'rb') as f:
            data = f.read()
        data = bytearray(data)
        for key in keys:
            test_data = data.copy()
            #decrypting data using XOR operation
            for index, value in enumerate(test_data):
                test_data[index] = value ^ int(key)
            #writing decrypted data
            with open(self.fname, 'wb') as f:
                f.write(test_data)
            if access(self.fname, R_OK):
                print(key)
                self.info_label.setText('File recovered successfully')
            else:
                self.info_label.setText('Not found')
     
        return None

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())