#!/usr/bin/env python3

from functools import partial
import sys
from PyQt5.QtCore import QRect, QMetaObject
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QPushButton
from PyQt5.uic import loadUi

class Keyboard(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = loadUi('./keyboard.ui')
        self.ui.show()

        self.buttons = {}

    def print_name(self, name):
        print(name)

    def connect_buttons(self):
        for b in self.buttons.keys():
            button = self.buttons[b]
            button.clicked.connect(partial(self.print_name, b))
            button.show()

    def add_buttons(self):
        with open('reddragon.ini', 'r') as keyfile:
            lines = keyfile.readlines()
            for line in lines:
                item = line.split(',')

                name = item[0]
                label = item[1]
                x = int(item[2]) + 50
                y = int(item[3]) + 50
                w = int(item[4])
                h = int(item[5])

                button = QPushButton(self.ui.buttons)
                button.setObjectName("key_" + name)
                button.setGeometry(QRect(x, y, w, h))
                button.setText(label)
                self.buttons[name] = button

def main():
    app = QApplication(sys.argv)

    kb = Keyboard()
    kb.add_buttons()
    kb.connect_buttons()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
