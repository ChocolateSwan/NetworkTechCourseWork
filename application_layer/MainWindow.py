from PyQt5.QtWidgets import (QWidget, QErrorMessage, QHBoxLayout)
from application_layer.LoginWindow import LoginWindow
from application_layer.ConversationWindow import ConversationWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.login_window = LoginWindow()
        self.conversation_window = ConversationWindow()

        self.login_window.connect_button.clicked.connect(self.connect_button_pressed)
        self.conversation_window.send_button.clicked.connect(self.send_button_pressed)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.login_window)
        main_layout.addWidget(self.conversation_window)
        self.conversation_window.hide()

        self.setLayout(main_layout)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Чатик')
        self.show()

    def connect_button_pressed(self):
        errors = self.login_window.validate()
        if len(errors) != 0:
            error_message = QErrorMessage()
            error_message.setWindowTitle('Ошибка')
            error_message.setFixedSize(550, 300)
            error_message.showMessage('<br>'.join(errors))
            error_message.exec_()
        else:
            self.connect()
            self.login_window.hide()
            self.conversation_window.show()
            self.setGeometry(300, 300, 650, 400)

    def send_button_pressed(self):
        pass

    def connect(self):
        self.conversation_window.chat_edit.setText('<p style="color:red;"> ОШИБКА </p>')
        pass
