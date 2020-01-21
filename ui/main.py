#!/usr/bin/env python3

import sys
from functools import partial

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.uic import loadUi

class Keyboard(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.ui = loadUi('./keyboard.ui')
        self.ui.show()

        self.buttons = {}
        self.active_color = [0, 0, 0]
        self.color_dialog = QColorDialog()

        self.bus = QDBusConnection.sessionBus()
        self.kb = QDBusInterface('com.qtech.openkeyboard.test', '/com/qtech/openkeyboard/test', 'com.qtech.openkeyboard.test.properties', QDBusConnection.sessionBus())

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb.call('SetBrightness', val)

    @pyqtSlot(int)
    def on_set_effect(self, val):
        print(val)
        self.kb.call('SetEffect', val)

    @pyqtSlot()
    def open_color_dialog(self):
        dialog = self.color_dialog.getColor()
        self.set_active_color(dialog.red(), dialog.green(), dialog.blue())
        self.set_color(self.ui.set_color)

    def set_active_color(self, r, g, b):
        self.active_color = [ r, g, b ]

    def set_color(self, button):
        col = self.active_color
        color = f'rgb({col[0]}, {col[1]}, {col[2]})'
        button.setStyleSheet('QPushButton { background-color: ' + color + ' }')

    def connect_buttons(self):
        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_color.clicked.connect(self.open_color_dialog)

        for b in self.buttons.keys():
            button = self.buttons[b]
            button.clicked.connect(partial(self.set_color, self.buttons[b]))
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

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
