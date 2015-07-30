#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_abb_i2c_lib import BB_I2C
from etc_header import *
import sys
import time

#Reading the Value that to Written in TPS Register
TPS_WR_Value = hex(int(sys.argv[1]))	
	
#This Function enables MPSSE Mode and Initializes FTDI Device
d=BB_I2C(0)
d.DevConf(BAUD,MASK_VAL,ASYNC_MODE)

data = ['a','b','c','d','e','f','g','h']

#Start Cmd
TXACKBuf=[]
RXACKBuf=[]

d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0x80,0)	
TXACKBuf+=d.SendByte(10)
for i in range(8):
	TXACKBuf+=d.SendByte(int(data[i].encode('hex')))					
d.I2CStop_CMD()
'''
	
d.I2CStart_CMD()
TXACKBuf+=d.SendAddr(0xA0,0)		
TXACKBuf+=d.SendByte(10)	
d.I2CStart_CMD()			
TXACKBuf+=d.SendAddr(0xA0,1)			
dataReceived =d.ReadByteAK()
print dataReceived
'''
	

