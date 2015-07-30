#------------------------------------------------------------------------------
#Author - Hari Udayakumar h.udayakumar.ee@lantiq.com
#
#Refer INA219 Spec for Detailed Calculation on Current LSB Value
#Note the Current LSB Value choosen is 200e-6
#
#--------------------------------------------------------------------------------

from etc_abb_i2c_lib import BB_I2C
from etc_abb_i2c_lib.etc_header import *
from etc_abb_i2c_lib.etc_ina219 import *
import sys
import time

CAL = [20480,20480,20480]
CALV = [0,0,0]
CON_VAL ='0fff'

Current = []
Power   = []
for x,y in zip(Voltage,Resistor):
	Current.append(x/y)
	Power.append(x*x/y)

#print Current
#print Power	

#Enable Port 0 for FTDI Synchronous mode
d = BB_I2C(0)

#This Function Configures FTDI for Synchronous Mode and Initializes FTDI Device for Communication
d.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)

#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(3):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],CON_VAL,RW)
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],hex(CAL[i])[2:],RW)	
	
#Read INA219 Registers
INA219=[[],[],[]]
n=0    
for da in I2C_ADDR:
    INA219[n].append(da)
    for ra in range(6):
        INA219[n].append(INA219_Reg_RRead(d,(da<<1),INA219_REG[ra],RW))
    n=n+1
#print INA219

for ix in range(3):
	CAL[ix] = int((CAL[ix] * int(INA219[ix][5],16) * 200e-6)/Current[ix])
	CALV[ix] = int((int(INA219[ix][3],16) >>3) * 4.0)
   
print ""
print CAL
print CALV
print ""


#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(3):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],CON_VAL,RW)
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],hex(CAL[i])[2:],RW)	
	
#Read INA219 Registers
INA219=[[],[],[]]
n=0    
for da in I2C_ADDR:
    INA219[n].append(da)
    for ra in range(6):
        INA219[n].append(INA219_Reg_RRead(d,(da<<1),INA219_REG[ra],RW))
    n=n+1
print INA219


for ix in range(3):
    print (int(INA219[ix][3],16)>>3)*4
	
Check_Sum = 0
RVAL = 0xFFFF
Flash_data = [CAL[0],CALV[0],CAL[1],CALV[1],CAL[2],CALV[2],int(CON_VAL,16),RVAL,0x2014,0x0730,0x4855]
for g in Flash_data:
    Check_Sum = Check_Sum+ g

Flash_data.append(Check_Sum)
print Flash_data
	
# writing flash
for ix in range(12):
	out = INA219_Reg_Write(d,(FLD_ADDR[0]<<1),hex(2*ix)[2:],hex(Flash_data[ix])[2:],RW)
	print str(ix), hex(Flash_data[ix])

print "\n flash values" 
for ix in range(12):
    print str(ix), INA219_Reg_RRead(d,(FLD_ADDR[0]<<1),hex(2*ix)[2:],RW)


