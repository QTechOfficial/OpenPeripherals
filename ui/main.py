#!/usr/bin/env python3

import sys
from functools import partial
from enum import Enum

from dbus import DBus

from PyQt5.QtCore import QRect, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5.uic import loadUi

from utils import set_button_color
from key import Key

class Direction(Enum):
    MAIN = False
    ALT = True

class Keyboard(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.ui = loadUi('keyboard.ui')
        self.ui.show()

        self.keys = {}
        self.active_color = (255, 255, 255)
        self.effect_color = (255, 255, 255)
        self.color_dialog = QColorDialog()

        self.bus = DBus()
        tmp = self.bus.get_devices()[0]
        print(f'Using service {tmp}')
        self.kb_effect = self.bus.get_interface(tmp, 'effect')
        self.kb_dimmable = self.bus.get_interface(tmp, 'dimmable')
        self.kb_animation = self.bus.get_interface(tmp, 'animation')
        self.kb_keyboard = self.bus.get_interface(tmp, 'keyboard')

    def pull_settings(self):
        effect = self.kb_effect.GetEffect()
        brightness = self.kb_dimmable.GetBrightness()
        speed = self.kb_animation.GetSpeed()
        direction = self.kb_animation.GetDirection()
        rainbow = self.kb_effect.GetRainbow()
        effect_color = self.kb_effect.GetEffectColor()
        key_colors = self.kb_keyboard.GetAllColors()

        self.ui.set_effect.setCurrentIndex(effect)
        self.ui.set_brightness.setValue(brightness)
        self.ui.set_speed.setValue(speed)

        if direction == Direction.MAIN.value:
            self.ui.direction_main.setChecked(True)
        elif direction == Direction.ALT.value:
            self.ui.direction_alt.setChecked(True)

        self.ui.set_rainbow.setCheckState(2 if rainbow else 0)

        self.effect_color = effect_color
        set_button_color(self.ui.set_effect_color, effect_color)

        for key_id, color in key_colors.items():
            self.keys[key_id].set_color(color)

    @pyqtSlot(int)
    def on_set_brightness(self, val):
        self.kb_dimmable.SetBrightness(val)

    @pyqtSlot(int)
    def on_set_effect(self, val):
        self.kb_effect.SetEffect(val)

    @pyqtSlot(int)
    def on_set_speed(self, val):
        self.kb_animation.SetSpeed(val)

    @pyqtSlot(int)
    def on_set_rainbow(self, val):
        self.kb_effect.SetRainbow(val > 0)

    @pyqtSlot()
    def on_direction_toggled(self):
        if self.ui.direction_main.isChecked():
            self.kb_animation.SetDirection(Direction.MAIN.value)
        elif self.ui.direction_alt.isChecked():
            self.kb_animation.SetDirection(Direction.ALT.value)

    @pyqtSlot()
    def on_set_all(self):
        color_data = {}
        for key_id, key in self.keys.items():
            set_button_color(key.button, self.active_color)
            color_data[key_id] = self.active_color

        self.kb_keyboard.SetAllColors(color_data)

    @pyqtSlot()
    def on_change_primary_color(self):
        col = self.color_dialog.getColor()
        self.active_color = (col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_active_color, self.active_color)

    @pyqtSlot()
    def on_change_effect_color(self):
        col = self.color_dialog.getColor()
        self.effect_color = (col.red(), col.green(), col.blue())
        set_button_color(self.ui.set_effect_color, self.effect_color)
        self.kb_effect.SetEffectColor(self.effect_color)

    @pyqtSlot(str, tuple)
    def on_set_key_color(self, key_id):
        self.kb_keyboard.SetKeyColor(key_id, self.active_color)
        self.keys[key_id].set_color(self.active_color)

    def connect_buttons(self):
        self.ui.set_effect.currentIndexChanged.connect(self.on_set_effect)

        self.ui.set_brightness.valueChanged.connect(self.on_set_brightness)
        self.ui.set_speed.valueChanged.connect(self.on_set_speed)

        self.ui.set_rainbow.stateChanged.connect(self.on_set_rainbow)

        self.ui.direction_main.toggled.connect(self.on_direction_toggled)
        self.ui.direction_alt.toggled.connect(self.on_direction_toggled)

        self.ui.set_active_color.clicked.connect(self.on_change_primary_color)
        self.ui.set_effect_color.clicked.connect(self.on_change_effect_color)
        self.ui.set_all.clicked.connect(self.on_set_all)

        for key_id in self.keys.keys():
            button = self.keys[key_id].button
            button.clicked.connect(partial(self.on_set_key_color, key_id))

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
                button.show()
                self.keys[name] = Key(name, button, led_offset)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    kb = Keyboard()
    kb.add_buttons()
    kb.connect_buttons()
    kb.pull_settings()

    sys.exit(app.exec())
