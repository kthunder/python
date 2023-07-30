import serial
import serial.tools.list_ports
from time import sleep
from pprint import pprint
import time
import binascii

for port in list(serial.tools.list_ports.comports()):
    pprint(port.device)

def recive():
    ser = serial.Serial("COM44", 115200)
    print("port state : ", ser.is_open)
    while True:
        print(ser.readline().decode('utf-8'))

def trans():
    ser = serial.Serial("COM48", 115200)
    print("port state : ", ser.is_open)
    string = '''0123456789ABCDEF'''+'\n'
    print(string.encode('utf-8').__len__())
    while True:
        time.sleep(1)
        ser.write(string.encode('utf-8'))

def bin_to_hex():
    # filename = "C:\\GIT\\Github\\python\\PySerial\\FLS.xmind"
    filename = "C:\\GIT\\Github\\python\\PySerial\\data.txt"
    content = "0"
    with open(filename, "rb") as f:
        content  = f.read().hex()
    array = []
    for index in range(0, len(content), 2):
        array.append(content[index: index+2])

def hex_to_bin(hex_str):
    array = []
    for index in range(0, len(hex_str), 2):
        array.append(hex_str[index: index+2])
    return bytes(int(x, 16) for x in array)

# trans()
filename1 = "C:\\GIT\\Github\\python\\PySerial\\dataw.txt"
with open(filename1, "wb") as f:
    bin_str = hex_to_bin("31323334353637383930")
    print(bin_str)
    f.write(bin_str)
