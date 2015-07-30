#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
#------------------------------------------------------------------------------
#Author - Hari Udayakumar h.udayakumar.ee@lantiq.com
#
#Refer INA219 Spec for Detailed Calculation on Current LSB Value
#Note the Current LSB Value choosen is 200e-6
#
#--------------------------------------------------------------------------------
from etc_abb_i2c_lib import BB_I2C
from etc_abb_i2c_lib.etc_header import *
import sys
import time


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


def etc_pwr(d):
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		Readings=[[],[],[]]
		for j in range(3):
			Readings[j].append(hex(I2C_ADDR[j])) 
			for i in range(6):
				Readings[j].append(INA219_Reg_RRead(d,(I2C_ADDR[j]<<1),INA219_REG[i]))
		return Readings

#This Function enables Synchronous Bit Bang Mode and Initializes FTDI Device
d=BB_I2C(0)
d.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)

'''
#print "\n flash values" 
Flash_data=[]
for ix in range(12):
	Flash_data.append(INA219_Reg_RRead(d,(FLD_ADDR[0]<<1),hex(2*ix)[2:]))
	#print hex(2*ix)[2:],Flash_data[ix]

conf_val = Flash_data[6]
while len(conf_val) < 4:
	conf_val = '0'+conf_val

if (int(conf_val,16) == 0) or (int(conf_val,16) == 0xffff):
        print "Callibration info not found"
cal_val = [Flash_data[0],Flash_data[2],Flash_data[4]]	


#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(3):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],conf_val)
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],cal_val[i])
'''	
Power_MM=[]
for j in range(3):
	dataBV=[]
	for i in range(6):
		data = INA219_Reg_RRead(d,(I2C_ADDR[j]<<1),INA219_REG[i])
		if i == 1:
			dataBV += round((int(data,16)*0.01),4),
		elif i == 2:
			dataBV += round((int(data,16)>>3)*0.004,4),
		elif i == 3:
			dataBV += round((int(data,16)*PWR_LSB[j]),4),
		elif i == 4:
			dataBV += round((int(data,16)*CUR_LSB[j]),4),
		else:
			dataBV += data,	
	Power_MM += dataBV,	
#Printing all the Results Read
print("\tAddr\tBV(V)\tSV(mV)\tCurrent(mA)\tPower(mW)")
print("Analog:")
for i in range(3):
		print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),Power_MM[i][2],Power_MM[i][1],(Power_MM[i][1]/0.01),Power_MM[i][3]))
		

		
