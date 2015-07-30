#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_ftdi import MPSSE_I2C
import time

WR=0
RD=1
SlaveAddr=0xA0
TWordAddr='1000'
RWordAddr='2000'
inp="Hello World!"
TXData=['31','32','33','34','35','36','37','38']
TXACKBuf=[]
RXACKBuf=[]
RXData=[]

#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()

#Data Transmission
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(SlaveAddr,WR)
TXACKBuf+=d.SendByte(TWordAddr[0:2])
TXACKBuf+=d.SendByte(TWordAddr[2:])
for i in range(len(TXData)):
	TXACKBuf+=d.SendByte(TXData[i]) 
d.I2CStop_CMD()
print TXACKBuf
time.sleep(0.1)

#DataReception
print RXData
d.I2CStart_CMD()
RXACKBuf+=d.SendAddr(SlaveAddr,WR)
RXACKBuf+=d.SendByte(RWordAddr[0:2])
RXACKBuf+=d.SendByte(RWordAddr[2:])
d.I2CStart_CMD()
RXACKBuf+=d.SendAddr(SlaveAddr,RD)
for i in range(8):
	RXData+=d.ReadByteAK()	
RXData+=d.ReadByteNAK()
d.I2CStop_CMD()
print RXData




