#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_ftdi import MPSSE_I2C
from etc_header import *
import time

#DataReception
def INA219_Reg_Read(SlaveAddr):
	RXACKBuf=[]
	RXData=[]
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(SlaveAddr,RD)
	RXData+=d.ReadByteAK()	
	RXData+=d.ReadByteNAK()
	d.I2CStop_CMD()
	return RXData	

def INA219_Reg_RRead(SlaveAddr,Reg):
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

def INA219_Ptr_Write(SlaveAddr,Reg):
	TXACKBuf=[]
	d.I2CStart_CMD()	
	TXACKBuf+=d.SendAddr(SlaveAddr,WR)
	TXACKBuf+=d.SendByte(Reg)
	d.I2CStop_CMD()
	return TXACKBuf
	
def INA219_Reg_Write(SlaveAddr,Reg,Data):
	TXACKBuf=[]
	d.I2CStart_CMD()
	TXACKBuf+=d.SendAddr(SlaveAddr,WR)	
	TXACKBuf+=d.SendByte(Reg)
	TXACKBuf+=d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
	TXACKBuf+=d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
	d.I2CStop_CMD()
	return TXACKBuf
	
#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()
'''
#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write((I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write((I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])
	
#Reading Shunt Voltage across All INA219
dataSV=[]
for i in range(6):
	data =INA219_Reg_RRead((I2C_ADDR[i]<<1),INA219_REG[1])
	dataSV += round(int(data.encode('hex'),16)*0.01,2),
	#print("Shunt Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[i],Voltage))	


#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
dataBV=[]
for i in range(6):
	data =INA219_Reg_RRead((I2C_ADDR[i]<<1),INA219_REG[2])
	dataBV += round(float(int(data.encode('hex'),16)>>3)*0.004,2),
	#print("Bus Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[i],Voltage))

#Reading Power Value across All INA219
dataPW=[]
for i in range(6):
	data=INA219_Reg_RRead((I2C_ADDR[i]<<1),INA219_REG[3])
	dataPW += round(float(int(data.encode('hex'),16))*(PWR_LSB[i]),2),
	#print("Current Register at I2C device addr - 0x%x is %f mAmps"%(I2C_ADDR[i],Current))	

dataCA=[]	
#Reading Current across All INA219
for i in range(6):
	data=INA219_Reg_RRead((I2C_ADDR[i]<<1),INA219_REG[4])
	dataCA += round(float(int(data.encode('hex'),16))*CUR_LSB[i],2),
	#print("Current Register at I2C device addr - 0x%x is %f mAmps"%(I2C_ADDR[i],Current))	

#Printing all the Results Read
print("\tAddr\tBV(V)\tSV(mV)\tCurrent(mA)\tPower(mW)")
print("Analog:")
for i in range(6):
		print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),dataBV[i],dataSV[i],dataCA[i],dataPW[i]))
		if i==2:
			print("\n\nDigital:")
			
'''			


	

