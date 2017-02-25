

class LogicalConnection:
    def __init__(self,
                 username,
                 inport_name,
                 inport_baudrate,
                 outport_name,
                 outport_baudrate):
        # Колбек для получения сообщения.
        # Два аргумента: отправитель и сообщение
        self.on_received = None
        # Колбек для сообщения о таймауте
        # Аргументы уточнить
        self.on_timed_out = None
        # Колбек для случая, когда направленное сообщение пришло двоим
        # иначе говоря, в системе имеется конфликт имен
        # Аргументы: сообщение и конфликтное имя
        self.on_conflict = None
        # Колбек для случая, когда направленное сообщение не дошло до адресата
        # Аргументы: сообщение и имя
        self.recipient_not_found = None
        # Колбек для случая, когда широковещательное дошло не до всех
        # Аргументы: сообщение
        self.broadcast_failed = None

    def send(self, recipient, message):
        if recipient == 'all':
            # широковещательное
            pass
        else:
            # нешироковещательное
            pass