#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_ftdi import MPSSE_I2C
from etc_header import *
import time
import sys

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
	
#Reading the Value that to Written in TPS Register
TPS_WR_Value = hex(int(sys.argv[1]))	
TPS_WR_Value = TPS_WR_Value[2:] + "00"

#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()

#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])
	
#Program TPS Device with the Required Value	
data=INA219_Reg_Write(d,(TPS_ADDR[1]<<1),"01",TPS_WR_Value)	

#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
data = INA219_Reg_RRead(d,(I2C_ADDR[3]<<1),INA219_REG[2])
data.encode('hex')
dataBV = round((int(data.encode('hex'),16)>>3)*0.004,4)

#Printing all the Results Read
print("\t\tAddr\tBV(V)")
print("Digital:")
print("\t\t%s\t%.2f"%(hex(I2C_ADDR[3]),dataBV))