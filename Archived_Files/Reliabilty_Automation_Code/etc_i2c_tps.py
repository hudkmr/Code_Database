#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_abb_i2c_lib.etc_header import *

#DataReception
def INA219_Reg_Read(d,SlaveAddr):
	RXACKBuf=[]
	RXData=[]
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(d,SlaveAddr,RD)
	RXData+=d.ReadByteAK()	
	RXData+=d.ReadByteNAK()
	d.I2CStop_CMD()
	return RXData	

def INA219_Reg_RRead(d,SlaveAddr,Reg):
	RXACKBuf=[]
	RXData=""
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(SlaveAddr,WR)
	RXACKBuf+=d.SendByte(Reg)
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(SlaveAddr,RD)
	RXData+=d.ReadByteAK()	
	RXData+=d.ReadByteNAK()
	d.I2CStop_CMD()
	return RXData	
	
def INA219_Reg_Write(d,SlaveAddr,Reg,Data):
	TXACKBuf=[]
	d.I2CStart_CMD()
	TXACKBuf+=d.SendAddr(SlaveAddr,WR)	
	TXACKBuf+=d.SendByte(Reg)
	TXACKBuf+=d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
	TXACKBuf+=d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
	d.I2CStop_CMD()
	return TXACKBuf	
