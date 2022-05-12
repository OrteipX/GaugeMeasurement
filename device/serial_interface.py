# Program Name: serial_interface.py
# Date: Jan 21, 2020

import serial
from enum import Enum
from collections import deque


class ErrorCode(Enum):
    NoError = 1
    TryAgain = 2
    FatalError = 3


class SerialInterface:

    __encoding = "ascii"
    __ser_buf = deque()
    __try_again = 0
    __command_len = 0

    def __init__(self, port, baudrate=57600, timeout=0.5):
        self.__port = port
        self.__baudrate = baudrate
        self.__timeout = timeout
        self.__ser_conn = serial.Serial()

    @property
    def port(self):
        return self.__port

    @port.setter
    def set_port(self, value):
        self.__port = value

    @property
    def baudrate(self):
        return self.__baudrate

    @baudrate.setter
    def set_baudrate(self, value):
        self.__baudrate = value

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def set_timeout(self, value):
        self.__timeout = value

    def connect(self):
        self.__ser_conn.port = self.__port
        self.__ser_conn.baudrate = self.__baudrate
        self.__ser_conn.timeout = self.__timeout

        try:
            if not self.__ser_conn.is_open:
                self.__ser_conn.open()
                print("Serial connected...\n")

            return self.__ser_conn

        except Exception as e:
            print("Error open serial port: {}\n".format(str(e)))
            exit()

    def __del__(self):
        self.__ser_conn.close()
        if not self.__ser_conn.is_open:
            print("Serial disconnected...\n")

    def remove_left_zeros(self, response=deque()):
        if len(response) > 0:
            while True:
                if response[0] != str(0):
                    break

                response.popleft()

        return response

    def copy_and_advance_buffer(self):
        response = deque(self.__ser_buf)

        if response != 0:
            for i in range(len(self.__ser_buf)):
                self.__ser_buf.pop()
                if i < 4:
                    response.popleft()

            response.pop()

            response = self.remove_left_zeros(response)

        return str().join(response)

    def parse_buffer(self):
        if len(self.__ser_buf) < self.__command_len:
            return ErrorCode.TryAgain, 0

        if self.__ser_buf[0] != "0" and self.__ser_buf[1] != "1" and \
                self.__ser_buf[2] != "A" and self.__ser_buf[3] != "+":
            print("FatalError")
            return ErrorCode.FatalError, 0

        return ErrorCode.NoError, self.copy_and_advance_buffer()

    def read_from_serial(self):
        serial_read = self.__ser_conn.read(128)

        return serial_read

    def read_response(self):
        bytes_read = self.read_from_serial()

        if len(bytes_read) < 0:
            return ErrorCode.FatalError, 0
        elif len(bytes_read) == 0:
            return ErrorCode.TryAgain, 0

        for ser in str(bytes_read.decode(self.__encoding)):
            self.__ser_buf.append(ser)

        return self.parse_buffer()

    def send_request(self, command):
        self.__ser_conn.write(str.encode(command))
