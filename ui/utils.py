def set_button_color(button, color):
    col = f'rgb({color.r}, {color.g}, {color.b})'
    button.setStyleSheet('QPushButton { background-color: ' + col + ' }')
