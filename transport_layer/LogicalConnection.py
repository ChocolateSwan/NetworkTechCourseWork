

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
        return self.username+'\0'+ resipient+'\0'+'0'+'\0'+'\0'+msg+'\0'


    def make_cyclic_code (self, vector):
        return (vector<<4)^self.division(vector<<4)


    def make_binary_code (self, symbol):
        return (str(bin(ord(symbol)))[2:10]).rjust(8,'0')


    def send(self, recipient, message): #massage - строка макса

        message=self.wrap(recipient,message)

        binary_string=""
        encoded_message=""

        # создание массива бинарных кодов
        for i in message:
            binary_string+= self.make_binary_code(i)

        #кодирование каждых 11-ти символов цикличесим кодом [11,15], запись символов с данными кодами в строку
        for j in (binary_string[i:i + 11] for i in range(0, len(binary_string), 11)): #вроде должно работать
            encoded_message+=chr(self.make_cyclic_code(int(j,base=2)))
        print(encoded_message)

        #маше(encoded_message.encode('utf-8'))




print(bin(ord('a')))
obj= LogicalConnection("user","port_in",100,"port_out",200)
print(obj.wrap('all','fghjk'))
obj.send('user',"aaa")















