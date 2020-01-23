#!/usr/bin/env python3

import sys
from functools import partial
from xml.etree import ElementTree

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.QtGui import QPalette, QColor
from PyQt5.uic import loadUi

from utils import set_button_color
from objects.color import Color
from objects.key import Key

class Keyboard(QObject):
    DBUS_SERVICE = 'com.qtech.openkeyboard'
    DBUS_INT_LEDS = DBUS_SERVICE + '.Leds'
    DBUS_PATH = '/com/qtech/openkeyboard'
    DBUS_PROPERTIES = 'org.freedesktop.DBus.Properties'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.ui = loadUi('keyboard.ui')
        self.ui.show()

        self.keys = {}
        self.active_color = Color(255, 255, 255)
        self.effect_color = Color(255, 255, 255)
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

    def get_all_colors(self, key_colors):
        for key_id in key_colors.keys():
            color = key_colors[key_id]
            self.set_key_color(key_id, Color(color[0], color[1], color[2]))

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb_leds.call('SetBrightness', val)

    @pyqtSlot(int)
    def on_set_effect(self, val):
        self.kb_leds.call('SetEffect', val)

    @pyqtSlot(str, Color)
    def set_key_color(self, key_id, color):
        self.kb_leds.call('SetKeyColor', self.keys[key_id].led_offset, color.r, color.g, color.b)
        self.keys[key_id].set_color(color)

    @pyqtSlot()
    def on_set_all(self):
        for key_id in self.keys.keys():
            self.set_key_color(key_id, self.active_color)

    @pyqtSlot()
    def on_change_primary_color(self):
        col = self.color_dialog.getColor()
        self.active_color.set(col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_color, self.active_color)

    @pyqtSlot()
    def on_change_effect_color(self):
        col = self.color_dialog.getColor()
        self.effect_color.set(col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_effect_color, self.effect_color)
        self.kb_leds.call('SetEffectColor', self.effect_color.r, self.effect_color.g, self.effect_color.b)

    def connect_buttons(self):
        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_color.clicked.connect(self.on_change_primary_color)
        self.ui.set_effect_color.clicked.connect(self.on_change_effect_color)
        self.ui.set_all.clicked.connect(self.on_set_all)

        for key_id in self.keys.keys():
            button = self.keys[key_id].button
            button.clicked.connect(partial(self.set_key_color, key_id, self.active_color))
            button.show()

    def add_buttons(self):
        with open('reddragon.def', 'r') as keyfile:
            lines = keyfile.readlines()
            for line in lines:
                item = line.split(',')

                name = item[0]
                label = item[1]
                x = int(item[2])
                y = int(item[3])
                w = int(item[4])
                h = int(item[5])
                led_offset = int(item[6])

                button = QPushButton(self.ui.buttons)
                button.setObjectName("key_" + name)
                button.setGeometry(QRect(x, y, w, h))
                button.setText(label)
                self.keys[name] = Key(name, button, led_offset)


def main():
    app = QApplication(sys.argv)

    kb = Keyboard()
    kb.add_buttons()
    kb.connect_buttons()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
