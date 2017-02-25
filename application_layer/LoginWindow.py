from os.path import isfile
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QComboBox, QGridLayout, QPushButton)


class LoginWindow(QWidget):
    default_baudrate_index = 6
    available_baudrates = [
        75,
        110,
        300,
        1200,
        2400,
        4800,
        9600,
        19200,
        38400,
        57600,
        115200
    ]

    def __init__(self):
        super().__init__()
        # Окно логина
        self.nickname_label = None
        self.outport_label = None
        self.inport_label = None
        self.nickname_edit = None
        self.outport_edit = None
        self.inport_edit = None
        self.inport_baudrate = None
        self.outport_baudrate = None
        self.connect_button = None
        self.login_layout = None

        self.init_login_ui()
        self.setLayout(self.login_layout)

    def init_login_ui(self):
        self.nickname_label = QLabel('Имя')
        self.outport_label = QLabel('Вых.порт')
        self.inport_label = QLabel('Вх.порт')

        self.nickname_edit = QLineEdit()
        self.outport_edit = QLineEdit()
        self.inport_edit = QLineEdit()

        self.inport_baudrate = QComboBox()
        self.outport_baudrate = QComboBox()
        self.connect_button = QPushButton('Присоединиться')

        self.inport_baudrate.addItems(map(lambda x: str(x), self.available_baudrates))
        self.inport_baudrate.setCurrentIndex(self.default_baudrate_index)
        self.outport_baudrate.addItems(map(lambda x: str(x), self.available_baudrates))
        self.outport_baudrate.setCurrentIndex(self.default_baudrate_index)

        self.login_layout = QGridLayout()
        self.login_layout.setSpacing(10)

        self.login_layout.addWidget(self.nickname_label, 1, 0)
        self.login_layout.addWidget(self.nickname_edit, 1, 1)

        self.login_layout.addWidget(self.outport_label, 2, 0)
        self.login_layout.addWidget(self.outport_edit, 2, 1)
        self.login_layout.addWidget(self.outport_baudrate, 3, 1)

        self.login_layout.addWidget(self.inport_label, 4, 0)
        self.login_layout.addWidget(self.inport_edit, 4, 1)
        self.login_layout.addWidget(self.inport_baudrate, 5, 1)

        self.login_layout.addWidget(self.connect_button, 6, 1)

    def validate(self):
        errors = []
        if len(self.nickname_edit.text()) == 0:
            errors.append('Пожалуйста, укажите имя')

        if len(self.inport_edit.text()) == 0:
            errors.append('Пожалуйста, укажите входной порт')
        elif not isfile(self.inport_edit.text()):
            errors.append('Не удалось найти указанный входной порт')

        if len(self.outport_edit.text()) == 0:
            errors.append('Пожалуйста, укажите выходной порт')
        elif not isfile(self.outport_edit.text()):
            errors.append('Не удалось найти указанный выходной порт')

        return errors
