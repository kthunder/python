from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice

import threading
import os
from time import sleep
import hashlib

def calculate_md5(filename):
    # 打开文件
    with open(filename, 'rb') as f:
        # 初始化md5 hash对象
        md5 = hashlib.md5()
        # 读取文件内容，并更新md5 hash
        for chunk in iter(lambda: f.read(128 * md5.block_size), b""):
            md5.update(chunk)
    # 返回md5 hash
    return md5.hexdigest()


# port_list = QSerialPortInfo.availablePorts()
# for port in port_list:
#     print(port.portName())
# port_0 = QSerialPortInfo(port_list[0].portName())

def ser_connect(port_name):
    ser = QSerialPort()
    ser.setPortName(port_name)
    ser.setBaudRate(1152000)  # 修改为你的波特率
    ser.setDataBits(QSerialPort.DataBits.Data8)  # 修改为你的数据位
    ser.setParity(QSerialPort.Parity.NoParity)  # 修改为你的奇偶校验位
    ser.setStopBits(QSerialPort.StopBits.OneStop)  # 修改为你的停止位
    ser.setFlowControl(QSerialPort.FlowControl.NoFlowControl)  # 修改为你的流控制设置
    if ser.open(QIODevice.OpenModeFlag.ReadWrite):
        print("conn succeed")
    else:
        print("conn failed")
    return ser

file_r = "../data.zip"
file_w = "../data1.zip"

def uart_recive():
    # ser = serial.Serial(COM_IN, 115200, timeout = 3)
    ser = ser_connect("COM3")
    counter = 0
    with open(file_w, "wb") as fw:
        while ser.waitForReadyRead(5000):
            content = ser.read(0x100)
            # print(f"read {len(content)} Bytes: {content}")
            counter += len(content)
            # print(f"revive block len : {len(content)} <<<")
            fw.write(content)
    print(f"===uart_recive over len : {counter}")
    ser.close()
    print(f'MD5 hash of {file_w}: {calculate_md5(file_w)}')
    return True

def uart_trans():
    # ser = serial.Serial(COM_OUT, 115200, timeout = 3
    ser = ser_connect("COM40")
    totle_size = os.path.getsize(file_r)
    print(f"===file totle size : {totle_size}")
    counter = 0
    with open(file_r, "rb") as fr:
        while content := fr.read(0x100):
            # print(f"send {len(content)} Bytes: {content}")
            counter += len(content)
            ser.write(content)
            ser.waitForBytesWritten(1000)
            print(f"===file totle size : {counter / totle_size * 100}")
    print(f"===uart_trans over len : {counter}")
    ser.close()
    print(f'MD5 hash of {file_r}: {calculate_md5(file_r)}')
    return True


if __name__ == "__main__":
    threading.Thread(target=uart_recive).start()
    # sleep(1)
    # threading.Thread(target=uart_trans).start()