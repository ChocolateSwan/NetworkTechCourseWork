import serial
import sys
import traceback
import threading
import serial.threaded

#arguments
#    port – Device name or None.
#    baudrate (int) – Baud rate such as 9600 or 115200 etc.
#    bytesize – Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
#    parity – Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
#    stopbits – Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
#    timeout (float) – Set a read timeout value.
#    xonxoff (bool) – Enable software flow control.
#    rtscts (bool) – Enable hardware (RTS/CTS) flow control. ALWAYS TRUE
#    dsrdtr (bool) – Enable hardware (DSR/DTR) flow control. ALWAYS TRUE
#    write_timeout (float) – Set a write timeout value.
#    inter_byte_timeout (float) – Inter-character timeout, None to disable (default).

#Raises:
#    ValueError – Will be raised when parameter are out of range, e.g. baud rate, data bits.
#    SerialException – In case the device can not be found or can not be configured.




class Connection:
    class PrintLines(serial.threaded.LineReader):
        on_received = None

        def connection_made(self, transport):
            super(Connection.PrintLines, self).connection_made(transport)
            sys.stdout.write('port opened\n')

        def data_received(self, data):
            self.on_received(data)
            #sys.stdout.write('Принято: {}\n'.format(repr(data)))

        def connection_lost(self, exc):
            if exc:
                traceback.print_exc(exc)
            sys.stdout.write('port closed\n')

    def __init__(self):
        self.ser = None
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.reading, args=(self.stop_event, ))
        self.on_received = None

    def connect(self, port_name, **kargs):
        self.ser = serial.Serial(port_name, rtscts=True, dsrdtr=True, **kargs)
        self.thread.start()

    def disconnect(self):
        self.stop_event.set()
        self.thread.join()
        self.ser.close()
        self.ser = None

    def is_connected(self):
        return self.ser is not None

    def reading(self, stop_event):
        with serial.threaded.ReaderThread(self.ser, Connection.PrintLines) as protocol:
            protocol.on_received = self.on_received
            while not stop_event.is_set():
                serial.time.sleep(0.1)

    def write(self, data):
        self.ser.write(data)

class TransportConnection:

    def __init__(self):
        self.on_received = None


if __name__ == '__main__':

    conn = Connection()
    conn.connect(sys.argv[1], baudrate=9600)

    conn.on_received = lambda x: print(x)

    message = ''
    while message != 'exit':
        serial.time.sleep(1)
        message = input('>>')
        conn.write(bytes(message, 'utf-8'))

    conn.disconnect()

