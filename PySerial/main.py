import serial
import serial.tools.list_ports
from time import sleep
from pprint import pprint
import threading

COM_IN = None
COM_OUT = None

ports = list(serial.tools.list_ports.comports())
if ports.__len__() >= 2:
    COM_IN = ports[0].device
    COM_OUT = ports[1].device

def print_ports():
    for port in list(serial.tools.list_ports.comports()):
        pprint(port.device)

file_r = "FLS.xmind"
file_w = "FLS1.xmind"
# file_r = "datar.txt"
# file_w = "dataw.txt"

def uart_recive():
    ser = serial.Serial(COM_IN, 115200, timeout = 3)
    print("port state : ", ser.is_open)
    ser.write("ready\n".encode('utf-8'))

    # while True:
    #     pass


    # with open(file_w, "wb") as fw:
    #     content = ser.read(0x100)
    #     while content:
    #         if len(content) != 0x100:
    #             print(len(content))
    #         fw.write(content)
    #         content = ser.read(0x100)
    print("uart_recive over")

def uart_trans():
    ser = serial.Serial(COM_OUT, 115200, timeout = 3)
    print("port state : ", ser.is_open)

    print(ser.read())

    # while  != "ready\n":
    #     pass

    # with open(file_r, "rb") as fr:
    #     content = fr.read(0x100)
    #     while content:
    #         if len(content) != 0x100:
    #             print(len(content))
    #         ser.write(content)
    #         content = fr.read(0x100)
    print("uart_trans over")

print_ports()

threading.Thread(target=uart_recive).start()
# sleep(0.5)
threading.Thread(target=uart_trans).start()