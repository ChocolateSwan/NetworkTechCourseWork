

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

    def division(self, rest):
        divider = 0b10011;
        while int.bit_length(rest) >= int.bit_length(divider):
            sub = divider
            while not (int.bit_length(rest) == int.bit_length(sub)):
                sub <<= 1
            rest ^= sub
        return rest


    def wrap (self,resipient, msg):
        return self.username+'\0'+ resipient+'\0'+'0'+'\0'+msg+'\0'


    def make_cyclic_code (self, vector):
        return (vector<<4)^self.division(vector<<4)


    def make_binary_code (self, symbol):
        return (str(bin(ord(symbol)))[2:10]).rjust(8,'0')


    def send(self, recipient, message): #massage - строка макса

        message=self.wrap(recipient,message)
        print(message)
        binary_string=""
        encoded_message=""

        # создание массива бинарных кодов
        for i in message:
            binary_string+= self.make_binary_code(i)
        print (binary_string)
        #кодирование каждых 11-ти символов цикличесим кодом [11,15], запись символов с данными кодами в строку
        for j in (binary_string[i:i + 11] for i in range(0, len(binary_string), 11)): #вроде должно работать
            encoded_message+=chr(self.make_cyclic_code(int(j,base=2)))
        print(encoded_message)
        print(encoded_message)
        return encoded_message.encode('utf-8') # переписать как маше(...)


    def find_error(self,rest):
        guess_error = 0b1  # Ищем ошибку
        rest_error = 0
        while rest_error != rest:
            rest_error = self.division(guess_error)
            guess_error <<=1
        return guess_error>>1


    def receive (self,message):
        message = message.decode('utf-8')
        binary_string=""
        decoded_message=""
        for i in message:
            rest = self.division(ord(i))
            if rest != 0:
                i=ord(i)^self.find_error(rest)
            binary_string+=(str(bin(ord(i)>>4))[2:13]).rjust(11,'0')
        print (binary_string)
        for j in (binary_string[i:i + 8] for i in range(0, len(binary_string), 8)):
           decoded_message+=chr(int(j,base=2))

        print(decoded_message)

        # почти работает !!!!!!!!!!!!!!!!!








print(bin(ord('a')))
obj= LogicalConnection("user","port_in",100,"port_out",200)
obj.receive(obj.send('user',"aaabb"))















