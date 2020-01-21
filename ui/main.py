#!/usr/bin/env python3

import sys
from functools import partial
from xml.etree import ElementTree

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.uic import loadUi

from color import Color

class Keyboard(QObject):
    DBUS_SERVICE = 'com.qtech.openkeyboard'
    DBUS_INT_LEDS = DBUS_SERVICE + '.Leds'
    DBUS_PATH = '/com/qtech/openkeyboard'
    DBUS_PROPERTIES = 'org.freedesktop.DBus.Properties'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.ui = loadUi('./keyboard.ui')
        self.ui.show()

        self.buttons = {}
        self.active_color = Color(0, 0, 0)
        self.effect_color = Color(0, 0, 0)
        self.color_dialog = QColorDialog()

        self.bus = QDBusConnection.sessionBus()
        tmp = self.get_devices()[0]
        print(f'Using service {tmp}')
        self.kb_leds = QDBusInterface(self.DBUS_SERVICE, self.DBUS_PATH + '/' + tmp, self.DBUS_INT_LEDS, self.bus)

    def get_devices(self):
        devices = []

        interface = QDBusInterface(self.DBUS_SERVICE, self.DBUS_PATH, 'org.freedesktop.DBus.Introspectable', self.bus)
        xml_str = interface.call('Introspect').arguments()[0]
        for child in ElementTree.fromstring(xml_str):
            if child.tag == 'node':
                devices.append(child.attrib['name'])

        return devices

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb_leds.call('SetBrightness', val)

    @pyqtSlot(int)
    def on_set_effect(self, val):
        self.kb_leds.call('SetEffect', val)

    @pyqtSlot()
    def color_button(self, button, color):
        col = self.color_dialog.getColor()
        color.set(col.red(), col.green(), col.blue())
        self.set_color(button, color)

    def set_color(self, button, color):
        col = f'rgb({color.r}, {color.g}, {color.b})'
        button.setStyleSheet('QPushButton { background-color: ' + col + ' }')

    def connect_buttons(self):
        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_color.clicked.connect(partial(self.color_button, self.ui.set_color, self.active_color))
        self.ui.set_effect_color.clicked.connect(partial(self.color_button, self.ui.set_effect_color, self.effect_color))

        for b in self.buttons.keys():
            button = self.buttons[b]
            button.clicked.connect(partial(self.color_button, button, self.active_color))
            button.show()

    def add_buttons(self):
        with open('reddragon.ini', 'r') as keyfile:
            lines = keyfile.readlines()
            for line in lines:
                item = line.split(',')

                name = item[0]
                label = item[1]
                x = int(item[2]) + 10
                y = int(item[3]) + 10
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
