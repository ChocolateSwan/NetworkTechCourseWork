from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton)


class ConversationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.chat_edit = None
        self.recipient_edit = None
        self.message_edit = None
        self.send_button = None
        self.conversation_layout = None
        self.init_main_ui()
        self.setLayout(self.conversation_layout)

    def init_main_ui(self):
        self.chat_edit = QTextEdit()
        self.recipient_edit = QLineEdit()
        self.message_edit = QLineEdit()
        self.send_button = QPushButton('Отпр.')

        self.chat_edit.setReadOnly(True)
        self.recipient_edit.setPlaceholderText('Получатель')
        self.message_edit.setPlaceholderText('Сообщение')

        message_widget = QWidget()
        message_layout = QHBoxLayout()
        message_layout.setSpacing(0)
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.addWidget(self.message_edit)
        message_layout.addWidget(self.send_button)
        message_widget.setLayout(message_layout)

        self.conversation_layout = QVBoxLayout()
        self.conversation_layout.addWidget(self.chat_edit)
        self.conversation_layout.addWidget(self.recipient_edit)
        self.conversation_layout.addWidget(message_widget)
        self.conversation_layout.setSpacing(10)
