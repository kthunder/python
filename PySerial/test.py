# QTserial
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice
from tqdm import tqdm


def open(port, baud):
    ser = QSerialPort()  # 修改为你的波特率
    ser.setPortName(port)  # 修改为你的波特率
    ser.setBaudRate(baud)  # 修改为你的波特率
    ser.setDataBits(QSerialPort.DataBits.Data8)  # 修改为你的数据位
    ser.setParity(QSerialPort.Parity.NoParity)  # 修改为你的奇偶校验位
    ser.setStopBits(QSerialPort.StopBits.OneStop)  # 修改为你的停止位
    ser.setFlowControl(QSerialPort.FlowControl.NoFlowControl)  # 修改为你的流控制设置
    ser.open(QIODevice.OpenModeFlag.ReadWrite)


if __name__ == "__main__":

    # 获取所有可用串口信息
    available_ports = QSerialPortInfo.availablePorts()

    # 打印每个串口的信息
    for port in available_ports:
        print(f"Port: {port.portName()}")
        print(f"Description: {port.description()}")
        print(f"Manufacturer: {port.manufacturer()}")
        print(f"System Location: {port.systemLocation()}")
        print(f"Serial Number: {port.serialNumber()}")
        print("")

# 000100011A5A5BB6000000000009DB09A5A5A5A597969908