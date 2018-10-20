import serial
import threading
import numpy


class DoubleVarContainer:
    def __init__(self, container):
        self.container = container

    def update(self, value):
        self.container.set(value)


class Reader:
    def __init__(self, port, dvar, size):
        self.arduino = serial.Serial(port, 115200, timeout=.1)
        self.dvar = DoubleVarContainer(dvar)
        self.t = None
        self.measures = [0 for i in range(int(size))]

    def start(self):
        self.t = threading.Thread(target=self.__read)
        self.t.daemon = True
        self.t.start()

    def __read(self):
        while True:
            data = self.arduino.read(10)

            if data:
                value = int.from_bytes(data, byteorder="little")
                self.dvar.update(value)
                self.measures.pop(0)
                self.measures.append(value)
