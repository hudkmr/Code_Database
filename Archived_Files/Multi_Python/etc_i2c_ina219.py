#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_ftdi import MPSSE_I2C
from etc_header import *
import time

#DataReception
def INA219_Reg_RRead(d,SlaveAddr,Reg):
	Noerror = 1
	while Noerror:
		RXData=""
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,WR)
		Noerror = d.SendByte(Reg)
		d.I2CStart_CMD()
		Noerror =d.SendAddr(SlaveAddr,RD)
		RXData+=d.ReadByteAK()	
		RXData+=d.ReadByteNAK()
		d.I2CStop_CMD()
	return RXData
	
def INA219_Reg_Write(d,SlaveAddr,Reg,Data):
	Noerror =1
	while Noerror:
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,WR)	
		Noerror = d.SendByte(Reg)
		Noerror = d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
		Noerror = d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
		d.I2CStop_CMD()
	return Noerror
	





	

