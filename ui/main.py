#!/usr/bin/env python3

import sys
from functools import partial
from xml.etree import ElementTree
from enum import Enum

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.QtGui import QPalette, QColor
from PyQt5.uic import loadUi

from utils import set_button_color
from objects.color import Color
from objects.key import Key

class Direction(Enum):
    MAIN = 0
    ALT = 1

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
        self.direction = Direction.MAIN

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
    def on_set_effect(self, val):
        self.kb_leds.call('SetEffect', val)

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb_leds.call('SetBrightness', val)

    @pyqtSlot(int)
    def on_set_speed(self, val):
        # self.kb_leds.call('SetSpeed', val)
        pass

    @pyqtSlot(int)
    def on_set_rainbow(self, val):
        if val:
            # ticked
            pass
        else:
            # unticked
            pass

    @pyqtSlot(bool)
    def on_set_direction_main(self, val):
        self.direction = Direction.MAIN
        # Call direction change

    @pyqtSlot(bool)
    def on_set_direction_alt(self, val):
        self.direction = Direction.ALT
        # Call direction change

    @pyqtSlot()
    def on_change_primary_color(self):
        col = self.color_dialog.getColor()
        self.active_color.set(col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_active_color, self.active_color)

    @pyqtSlot()
    def on_change_effect_color(self):
        col = self.color_dialog.getColor()
        self.effect_color.set(col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_effect_color, self.effect_color)
        self.kb_leds.call('SetEffectColor', self.effect_color.r, self.effect_color.g, self.effect_color.b)

    @pyqtSlot(str, Color)
    def on_set_key_color(self, key_id, color):
        self.kb_leds.call('SetKeyColor', self.keys[key_id].led_offset, color.r, color.g, color.b)
        self.keys[key_id].set_color(color)

    @pyqtSlot()
    def on_set_all_keys(self):
        for key_id in self.keys.keys():
            self.on_set_key_color(key_id, self.active_color)

    def get_all_colors(self):
        keys = {}
        for key_id in self.keys.keys():
            color = self.keys[key_id].color
            keys[key_id] = (color.r, color.g, color.b)
        return keys

    def set_all_colors(self, key_colors):
        for key_id in key_colors.keys():
            color = key_colors[key_id]
            self.on_set_key_color(key_id, Color(color[0], color[1], color[2]))

    def connect_buttons(self):
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_speed.valueChanged.connect(self.on_set_speed)

        self.ui.set_rainbow.stateChanged.connect(self.on_set_rainbow)

        self.ui.direction_main.clicked.connect(self.on_set_direction_main)
        self.ui.direction_alt.clicked.connect(self.on_set_direction_alt)

        self.ui.set_active_color.clicked.connect(self.on_change_primary_color)
        self.ui.set_effect_color.clicked.connect(self.on_change_effect_color)
        self.ui.set_all.clicked.connect(self.on_set_all_keys)

        for key_id in self.keys.keys():
            button = self.keys[key_id].button
            button.clicked.connect(partial(self.on_set_key_color, key_id, self.active_color))
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
                button.setObjectName('key_' + name)
                button.setGeometry(QRect(x, y, w, h))
                button.setText(label)
                self.keys[name] = Key(name, button, led_offset)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    kb = Keyboard()
    kb.add_buttons()
    kb.connect_buttons()

    sys.exit(app.exec())

