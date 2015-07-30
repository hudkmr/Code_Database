#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
#------------------------------------------------------------------------------
#Author - Hari Udayakumar h.udayakumar.ee@lantiq.com
#
#Refer INA219 Spec for Detailed Calculation on Current LSB Value
#Note the Current LSB Value choosen is 200e-6
#
#--------------------------------------------------------------------------------
from etc_ftdi import *
from etc_ftdi.etc_i2c_ina219 import *

etc_i2c = MPSSE_I2C(0)
etc_i2c.DevConf_I2C()
RXData=[]
#Read Register 00
etc_i2c.I2CStart_CMD()
Noerror = etc_i2c.SendAddr(0x90,0)
Noerror = etc_i2c.SendByte('01')
etc_i2c.I2CStart_CMD()
Noerror =etc_i2c.SendAddr(0x90,1)
RXData+=etc_i2c.ReadByteAK()	
RXData+=etc_i2c.ReadByteNAK()
etc_i2c.I2CStop_CMD()
print RXData


