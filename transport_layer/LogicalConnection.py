# Один исходный символ - один закодированный символ.

# Максу - имя не пустое и не all
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
    def wrap (self,resipient, msg, sender, counter):
        return sender+'\0'+ resipient+'\0'+str(counter)+'\0'+msg+'\0'

    # Циклическое кодирование.
    def make_cyclic_code (self, vector):
        return (vector<<4)^self.division(vector<<4)

    # Отправка сообщения.
    def send(self, recipient, message,**kwargs):    # massage - строка макса
        message = self.wrap(recipient, message,    # Обертка сообщения.
                            kwargs.get('sender',self.username), kwargs.get('counter', 0))
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

        #self.parse_message(decoded_message)    #Раскомментировать!!!!

    # Интерпретация сообщения.
    def parse_message(self, message):  # 0-отправитель, 1-получатель, 2-счетчик, 3-текст
        info_in_message = message.split("\0")
        # Ошибочный формат сообщения.
        if self.validate(info_in_message):

            if (info_in_message[0]==self.username and info_in_message[1]==self.username):
                pass    # ???????????????????????????????????????

            # Если сообщение адресовано нам.
            if (info_in_message[1] == self.username):
                #self.on_received(info_in_message[0], info_in_message[3])    # Раскомментировать!!!!
                info_in_message[2]=int(info_in_message[2])+1    # Увеличиваем счетчик принятых.
                self.send(info_in_message[1],info_in_message[3],
                          sender = info_in_message[0],counter = info_in_message[2])    # Отпраляем обратно

            # Если мы отправители.
            if (info_in_message[0]==self.username):
                if (info_in_message[1] == 'all'):    # Если послали всем.
                    if (int(info_in_message[2]) < 2):    # Если приняли не все.
                        pass
                        # self.broadcast_failed()    #Раскомментировать!!!
                else:    # Если отправляли направленно.
                    if (info_in_message[2] == "0"):    # Если адресат не принял
                        pass
                        #self.recipient_not_found()    #Раскомментировать!!!!
                    elif (info_in_message[2] == "2"):    # Если имеется конфликт имен.
                        pass
                        #self.on_conflict()    # Раскомментировать!!!!
        else:    # Если сообщение невалидно
            pass


    def validate (info_in_message):
        is_valid=True
        if (info_in_message[-1]!= '' or len(info_in_message)!=5): # Общая проверка.
            is_valid=False
        if (info_in_message[0]==""):    # Проверка отправителя.
            is_valid = False
        if (info_in_message[1]==""):    # Проверка получателя.
            is_valid = False
        if not((info_in_message[2]).isdigit()):    # Проверка счетчика.
            is_valid = False
        if (info_in_message[3]==""):    # Проверка cообщения.
            is_valid = False
        return is_valid








obj= LogicalConnection("user","port_in",100,"port_out",200)
obj.receive(obj.send('user',"ksmcvkvy"))















