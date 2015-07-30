#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
from etc_abb_i2c_lib import BB_I2C
from etc_abb_i2c_lib.etc_header import *
import sys
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
	
def INA219_Reg_Write(SlaveAddr,Reg,Data):
	TXACKBuf=[]
	d.I2CStart_CMD()
	TXACKBuf+=d.SendAddr(SlaveAddr,WR)	
	TXACKBuf+=d.SendByte(Reg)
	TXACKBuf+=d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
	TXACKBuf+=d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
	d.I2CStop_CMD()
	return TXACKBuf	

#Reading the Value that to Written in TPS Register
TPS_WR_Value = hex(int(sys.argv[1]))	
TPS_WR_Value = TPS_WR_Value[2:] + "00"

#This Function enables MPSSE Mode and Initializes FTDI Device
d=BB_I2C(0)
d.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)

#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write((I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write((I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])

#Program TPS Device with the Required Value	
data=INA219_Reg_Write((TPS_ADDR[0]<<1),TPS_REG[0],TPS_WR_Value)	
	
	
#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
dataBV=[]
for i in range(1):
	data =INA219_Reg_RRead((I2C_ADDR[0]<<1),INA219_REG[2])
	dataBV += round(float(int(data,16)>>3)*0.004,2),
	#print("Bus Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[i],Voltage))

#Printing all the Results Read
print("\t\tAddr\tBV(V)")
print("Analog:")
print("\t\t%s\t%.2f"%(hex(I2C_ADDR[0]),dataBV[0]))
