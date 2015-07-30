#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_abb_i2c_lib import BB_I2C
from etc_abb_i2c_lib.etc_header import *
import sys
import time


d=BB_I2C(0)
d.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)

TXACKBuf=[]
RXACKBuf=[]
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0x80,0)
TXACKBuf+=d.SendByte('00')
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0x80,1)
RXACKBuf+=d.ReadByteAK()
RXACKBuf+=d.ReadByteNAK()
d.I2CStop_CMD()
print RXACKBuf

'''
data = ['1','2','3','4','5','6','7','8']
TXACKBuf=[]
RXACKBuf=[]
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0xA6,0)	
TXACKBuf+=d.SendByte(0x10)
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0xA6,1)
for i in range(7):
	RXACKBuf+=d.ReadByteAK()	
RXACKBuf+=d.ReadByteNAK()	
d.I2CStop_CMD()	
print RXACKBuf
'''
