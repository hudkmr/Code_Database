#Basic I2C Commands for INA219 Current Shunt Monitors
from etc_header import *

def INA219_Reg_RRead(d,SlaveAddr,Reg):
	Noerror = 1
	while Noerror:
		RXData=""
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,WR)
		Noerror = d.SendByte(Reg)
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,RD)
		RXData+=d.ReadByteAK()	
		RXData+=d.ReadByteNAK()
		d.I2CStop_CMD()
	return RXData


	
def INA219_Reg_Write(d,SlaveAddr,Reg,Data):
	Noerror = 1
	while Noerror:
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,WR)	
		Noerror = d.SendByte(Reg)
		Noerror = d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
		Noerror = d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
		d.I2CStop_CMD()
	return Noerror

'''	
def INA219_Ptr_Write(d,SlaveAddr,Reg):
	TXACKBuf=[]
	d.I2CStart_CMD()	
	TXACKBuf+=d.SendAddr(SlaveAddr,WR)
	TXACKBuf+=d.SendByte(Reg)
	d.I2CStop_CMD()
	return TXACKBuf	

def INA219_Reg_Read(d,SlaveAddr):
	RXACKBuf=[]
	RXData=[]
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(d,SlaveAddr,RD)
	RXData+=d.ReadByteAK()	
	RXData+=d.ReadByteNAK()
	d.I2CStop_CMD()
	return RXData	
'''		