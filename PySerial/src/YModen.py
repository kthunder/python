from enum import Enum
import os
import sys
import math 
import time
# QTserial
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtCore import QIODevice
from tqdm import tqdm

class YmodemCtr(Enum):
    SOH    = 0x01 # start of 128-byte data packe
    STX    = 0x02 # start of 1024-byte data pack
    EOT    = 0x04 # end of transmission
    ACK    = 0x06 # acknowledge
    NAK    = 0x15 # negative acknowledge
    CAN    = 0x18 # two of these in succession a
    C      = 0x43 # request command
    ABORT1 = 0x41 # abort by user
    ABORT2 = 0x61 # abort by user


class YmodemFrame:  
    def __init__(self, header:YmodemCtr, sequence:int=0, data:bytes=[], pad=0x1A):
        if header not in YmodemCtr:
            raise TypeError("header type error")
        # if sequence > 0xFF:
        #     raise TypeError("sequence out of bound")
        if header == YmodemCtr.SOH and len(data) > 128:
            raise TypeError("data len overflow, max:128")
        elif header == YmodemCtr.STX and len(data) > 1024:
            raise TypeError("data len overflow, max:1024")
        
        frame_len = 0
        if header == YmodemCtr.SOH:
            frame_len = 128
        elif header == YmodemCtr.STX:
            frame_len = 1024

        self.header = header
        self.sequence = sequence&0xFF
        self.data = data
        self.padding = bytearray([pad]*(frame_len-len(data)))

    def to_bytes(self):  
        # 构建Ymodem包字节串
        if self.header in [YmodemCtr.SOH, YmodemCtr.STX]:
            frame = bytearray()
            frame.append(self.header.value) # Ymodem协议z帧头
            frame.append(self.sequence) # 序列号
            frame.append(~self.sequence&0xFF) # 序列号的反码
            frame.extend(self.data)
            frame.extend(self.padding)
            frame.extend(self.check_value())
        else:
            frame = bytearray()
            frame.append(self.header.value)
        return frame  

    def check_value(self):  
        # 计算校验和  
        return ( 0xFFFF).to_bytes(2)

class YModemTransfer:
    def __init__(self, port, baud=115200):
        ser = QSerialPort()                                        # 修改为你的波特率
        ser.setPortName(port)                                      # 修改为你的波特率
        ser.setBaudRate(baud)                                      # 修改为你的波特率
        ser.setDataBits(QSerialPort.DataBits.Data8)                # 修改为你的数据位
        ser.setParity(QSerialPort.Parity.NoParity)                 # 修改为你的奇偶校验位
        ser.setStopBits(QSerialPort.StopBits.OneStop)              # 修改为你的停止位
        ser.setFlowControl(QSerialPort.FlowControl.NoFlowControl)  # 修改为你的流控制设置
        if ser.open(QIODevice.OpenModeFlag.ReadWrite):
            self.ser = ser
        else:
            raise PermissionError(f'serial {port} open failed ...')
        pass


    def write(self, frame:YmodemFrame, time_out=10000) -> bool :
        # print("serial write : ",'[', frame.to_bytes(),']')
        self.ser.write(frame.to_bytes())
        return self.ser.waitForBytesWritten(time_out)

    # TODO
    def read(self, time_out=5000) -> YmodemFrame:
        while True:
            self.ser.waitForReadyRead(0)
            res = self.ser.read(1)
            if len(res) == 1:
                # print("serial read : ",'[', res,']')
                if (ctx:=res[0]) in YmodemCtr:
                    if ctx == YmodemCtr.SOH.value:
                        remained = 2 + 128 + 2
                        while remained > 0:
                            self.ser.waitForReadyRead(0)
                            temp = self.ser.read(remained)
                            remained -= len(temp)
                            res+=temp
                        return YmodemFrame(YmodemCtr.SOH,res[1],res[3:3+128])
                    if ctx == YmodemCtr.STX.value:
                        remained = 2 + 1024 + 2
                        while remained > 0:
                            self.ser.waitForReadyRead(0)
                            temp = self.ser.read(remained)
                            remained -= len(temp)
                            res+=(temp)
                        return YmodemFrame(YmodemCtr.STX,res[1],res[3:3+1024])
                    if ctx == YmodemCtr.EOT.value:
                        return YmodemFrame(YmodemCtr.EOT)
                    if ctx == YmodemCtr.ACK.value:
                        return YmodemFrame(YmodemCtr.ACK)
                    if ctx == YmodemCtr.NAK.value:
                        return YmodemFrame(YmodemCtr.NAK)
                    if ctx == YmodemCtr.CAN.value:
                        return YmodemFrame(YmodemCtr.CAN)
                    if ctx == YmodemCtr.C.value:
                        return YmodemFrame(YmodemCtr.C)
                    if ctx == YmodemCtr.ABORT1.value:
                        return YmodemFrame(YmodemCtr.ABORT1)
                    if ctx == YmodemCtr.ABORT2.value:
                        return YmodemFrame(YmodemCtr.ABORT2)
                else:
                    continue


    @staticmethod
    def first_frame(mode, file_name, file_size):
        x = YmodemCtr.SOH if mode == 128 else YmodemCtr.STX
        name = bytearray([ord(i) for i in file_name]+[0])
        size = bytearray([ord(i) for i in str(file_size)]+[0])
    
        return YmodemFrame(x, 0, name+size, pad=0)

    @staticmethod
    def data_frame(mode, file_data):
        x = YmodemCtr.SOH if mode == 128 else YmodemCtr.STX
        index=0
        while file_data:
            index+=1
            # print(index,"：",file_data[:10])
            yield YmodemFrame(x, index, file_data[:mode])
            file_data = file_data[mode:]


    @staticmethod
    def last_frame(mode):
        x = YmodemCtr.SOH if mode == 128 else YmodemCtr.STX
        return YmodemFrame(x, 0, [], pad=0)
    
    def send(self, file_path, mode=128):
        if not os.path.exists(file_path):
            print('file is not found')
            return False

        file_data = bytes()
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        print('wait for C')
        while self.read().header != YmodemCtr.C:
            pass

        first_frame = YModemTransfer.first_frame(mode, name, file_size)
        self.write(first_frame)

        while self.read().header != YmodemCtr.ACK:
            pass

        for data_frame in YModemTransfer.data_frame(mode, file_data):
            # print("send data frame>>>>>",data_frame[:2],data_frame[-2:])
            self.write(data_frame)
            if self.read().header == YmodemCtr.ACK:
                continue
            else:
                # print('error')
                return False

        EOT_frame = YmodemFrame(YmodemCtr.EOT)
        self.write(EOT_frame)

        while self.read(1).header != YmodemCtr.ACK:
            pass

        last_frame = YModemTransfer.last_frame(mode)
        self.write(last_frame)
        while self.read(1).header != YmodemCtr.ACK:
            pass

    def recv(self):
        self.write(YmodemFrame(YmodemCtr.C))
        file_name = ''
        file_size = 0
        count = 0
        
        while frame:=self.read():
            if frame.header == YmodemCtr.SOH or frame.header == YmodemCtr.STX:
                res = frame.data.split(bytearray([0]))
                file_name = res[0]
                file_size = int(res[1])
                print(file_name)
                print(file_size)
                self.write(YmodemFrame(YmodemCtr.ACK))
                break
        pbar = tqdm(total=file_size, unit='B', unit_scale=True)
        with open('b-'+str(file_name,encoding="UTF-8"),'wb') as f:
            while frame:=self.read():
                if frame.header in [YmodemCtr.SOH, YmodemCtr.STX]:
                    f.write(frame.data)
                    pbar.update(len(frame.data))
                    self.write(YmodemFrame(YmodemCtr.ACK))
                elif frame.header == YmodemCtr.EOT:
                    # print('recive EOT')
                    self.write(YmodemFrame(YmodemCtr.ACK))
                    break
        pbar.close()
        while frame:=self.read():
            if frame.header in [YmodemCtr.SOH, YmodemCtr.STX]:
                self.write(YmodemFrame(YmodemCtr.ACK))
                break

        print('recive succeed',count)


if __name__ == '__main__':
    if len(sys.argv)>=4:
        mode = sys.argv[1]
        baud = 115200*2**int(sys.argv[2])
        com = sys.argv[3]
        file = None
        if len(sys.argv)==5:
            file = sys.argv[4]

        if mode == 's':
            y_mode = YModemTransfer(com,baud)
            y_mode.send(file, mode=1024)
        elif mode == 'r':
            y_mode = YModemTransfer(com,baud)
            y_mode.recv()
        else:
            print("error arg")
