def set_button_color(button, color):
    col = f'rgb({color[0]}, {color[1]}, {color[2]})'
    button.setStyleSheet('QPushButton { background-color: ' + col + ' }')
