#!/usr/bin/env python3

import sys
from functools import partial
from xml.etree import ElementTree

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.uic import loadUi

from color import Color
from key import Key

class Keyboard(QObject):
    DBUS_SERVICE = 'com.qtech.openkeyboard'
    DBUS_INT_LEDS = DBUS_SERVICE + '.Leds'
    DBUS_PATH = '/com/qtech/openkeyboard'
    DBUS_PROPERTIES = 'org.freedesktop.DBus.Properties'

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.ui = loadUi('keyboard.ui')
        self.ui.show()

        self.buttons = {}
        self.active_color = Color(0, 0, 0)
        self.effect_color = Color(0, 0, 0)
        self.color_dialog = QColorDialog()

        self.bus = QDBusConnection.sessionBus()
        tmp = self.get_devices()[0]
        print(f'Using service {tmp}')
        self.kb_leds = QDBusInterface(self.DBUS_SERVICE, self.DBUS_PATH + '/' + tmp, self.DBUS_INT_LEDS, self.bus)
        self.pull_settings()

    def get_devices(self):
        devices = []

        interface = QDBusInterface(self.DBUS_SERVICE, self.DBUS_PATH, 'org.freedesktop.DBus.Introspectable', self.bus)
        xml_str = interface.call('Introspect').arguments()[0]
        for child in ElementTree.fromstring(xml_str):
            if child.tag == 'node':
                devices.append(child.attrib['name'])

        return devices

    def pull_settings(self):
        effect = self.kb_leds.call('GetEffect').arguments()[0]
        brightness = self.kb_leds.call('GetBrightness').arguments()[0]
        speed = self.kb_leds.call('GetSpeed').arguments()[0]
        direction = self.kb_leds.call('GetDirection').arguments()[0]
        rainbow = self.kb_leds.call('GetRainbow').arguments()[0]
        effect_color = self.kb_leds.call('GetEffectColor').arguments()
        key_colors = self.kb_leds.call('GetAllColors').arguments()[0]

        self.ui.set_effect.setCurrentIndex(effect)
        self.ui.set_brightness.setValue(brightness)
        self.effect_color = Color(*effect_color)
        self.set_button_color(self.ui.set_effect_color, Color(*effect_color))

    @staticmethod
    def set_button_color(button, color):
        col = f'rgb({color.r}, {color.g}, {color.b})'
        button.setStyleSheet('QPushButton { background-color: ' + col + ' }')

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb_leds.call('SetBrightness', val)

    @pyqtSlot(int)
    def on_set_effect(self, val):
        self.kb_leds.call('SetEffect', val)

    @pyqtSlot(str, Color)
    def set_key_color(self, button_id, color):
        self.kb_leds.call('SetKeyColor', self.buttons[button_id].led_offset, color.r, color.g, color.b)
        self.set_button_color(self.buttons[button_id].button, color)

    @pyqtSlot()
    def on_set_all(self):
        for button_id in self.buttons.keys():
            self.set_key_color(button_id, self.active_color)

    @pyqtSlot()
    def on_change_primary_color(self):
        col = self.color_dialog.getColor()
        self.active_color.set(col.red(), col.green(), col.blue())
        self.set_button_color(self.ui.set_color, self.active_color)

    @pyqtSlot()
    def on_change_effect_color(self):
        col = self.color_dialog.getColor()
        self.effect_color.set(col.red(), col.green(), col.blue())
        self.set_button_color(self.ui.set_effect_color, self.effect_color)
        self.kb_leds.call('SetEffectColor', self.effect_color.r, self.effect_color.g, self.effect_color.b)

    def connect_buttons(self):
        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_color.clicked.connect(self.on_change_primary_color)
        self.ui.set_effect_color.clicked.connect(self.on_change_effect_color)
        self.ui.set_all.clicked.connect(self.on_set_all)

        for button_id in self.buttons.keys():
            button = self.buttons[button_id].button
            button.clicked.connect(partial(self.set_key_color, button_id, self.active_color))
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
                self.buttons[name] = Key(name, button, led_offset)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    kb = Keyboard()
    kb.add_buttons()
    kb.connect_buttons()

    sys.exit(app.exec())
