# Один исходный символ - один закодированный символ.

class LogicalConnection:
    def __init__(self,
                 username, # пользователь
                 inport_name, # имя входного порта
                 inport_baudrate, # входная скорость передачи данных
                 outport_name, # имя выходного порта
                 outport_baudrate): # входная скорость передачи данных
        self.username = username
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
        #-------------------------------

    # Получение остатка от деления.
    def division(self, rest):
        divider = 0b10011;
        while int.bit_length(rest) >= int.bit_length(divider):
            sub = divider
            while not (int.bit_length(rest) == int.bit_length(sub)):
                sub <<= 1
            rest ^= sub
        return rest

    #Обертка сообщения.
    def wrap (self,resipient, msg):
        return self.username+'\0'+ resipient+'\0'+'0'+'\0'+msg+'\0'

    # Циклическое кодирование.
    def make_cyclic_code (self, vector):
        return (vector<<4)^self.division(vector<<4)

    # Отправка сообщения.
    def send(self, recipient, message):    # massage - строка макса
        message=self.wrap(recipient,message)
        encoded_message=""    # Закодированное сообщение.
        # Кодирование каждого символа циклическим кодом [11,15]
        for i in message:
            encoded_message +=chr(self.make_cyclic_code(ord(i)))
        return encoded_message.encode('utf-8') # переписать как маше(...)

    # Проверка на наличие ошибки (остаток от деления).
    def find_error(self,rest):
        guess_error = 0b1    # Предполагаемая ошибка.
        rest_error = 0
        while rest_error != rest:
            rest_error = self.division(guess_error)
            guess_error <<=1
        return guess_error>>1

    # Прием сообщения.
    def receive (self,message):
        message = message.decode('utf-8')
        decoded_message = ""    # Раскодированное сообщение.
        for i in message:
            rest = self.division(ord(i))    # Проверка на ошибку.
            if rest != 0:
                i = chr(ord(i) ^ self.find_error(rest))    # Попытка исправления ошибки.
            decoded_message += chr(ord(i) >> 4)
        print(decoded_message)    # Убрать потом!!!!

        self.parse_message(decoded_message)

    # Интерпретация сообщения.
    def parse_message(message):
        pass


obj= LogicalConnection("user","port_in",100,"port_out",200)
obj.receive(obj.send('user',"ksmcvkvy"))















