from etc_ftdi import MPSSE_I2C
from etc_header import *
import time

RXACKBuf=[]
RXData=[]
#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()


d.I2CStart_CMD()
RXACKBuf+=d.SendAddr(SlaveAddr,RD)
#RXACKBuf+=d.SendAddr('00')
RXData+=d.ReadByteAK()	
RXData+=d.ReadByteNAK()
d.I2CStop_CMD()
print RXData

