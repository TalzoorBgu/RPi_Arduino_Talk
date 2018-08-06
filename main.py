# main
from __future__ import print_function
import serial
import time
import curses
import thread
import sys

class SendCommand:
    def __init__(self, stp_pin, dir_pin, en_pin):
        self.stp_pin = stp_pin
        self.dir_pin = dir_pin
        self.en_pin = en_pin

    def init_seq(self):
        _str_to_send = ''
        return _str_to_send

    def move(self, _steps, _dir):
        _str_to_send = 'OK_move'
        return _str_to_send

    def moveto(self, _pos, _dir):
        _str_to_send = 'OK_moveto'
        return _str_to_send

    def define_vel_acc(self, _vel, _acc):
        _str_to_send = ''
        return _str_to_send


class MySerial:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)

    def write(self, cmd):
        if not cmd == '':
            print('Echo:{}'.format(cmd))
            self.ser.write(cmd.encode())
        return 'done'

    def read(self):
        ch_r_d = ''
        ch_r = ''
        try:
            nbChars = self.ser.in_waiting
            if nbChars > 0:
                time.sleep(0.05)
                nbChars = self.ser.in_waiting
                ch_r = self.ser.read(nbChars)
                ch_r = ch_r.decode()
        except:
            pass
        return ch_r


command = SendCommand(0, 1, 2)


def main():

    s = MySerial("/dev/ttyS0", 9600)
    i = 0
    while True:
        print("---m2---")
        i += 1
        time.sleep(0.05)
        result = s.read()

        if not result == '':
            print('Got:{0}'.format(result), end=' ')
            result_w = s.write('{}'.format(result))


def input_thread():
    # global key_pressed
    while True:
        key_pressed = read_key()
        print("Key pressed-{}".format(key_pressed))
        # print(key_pressed)
        if key_pressed == "q" or key_pressed == "Q":
            thread.interrupt_main()
            break
        else:
            res = command.move(100, 'R')
            print('res:{}'.format(res))


def read_key():
    import termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~(termios.ICANON | termios.ECHO)  # c_lflags
    c = None
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)
    return c


if __name__ == '__main__':
    print("---Started---")
    try:

        thread.start_new_thread(input_thread, ())  # ADDED

        i = 0
        flag_first_time = True
        while True:  # loop
            main()
            sys.stdout.flush()

    except KeyboardInterrupt:  # ADDED
        print("Quit")

    finally:
        sys.exit(0)
        print("Bye")
        pass
