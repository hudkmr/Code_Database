#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
#------------------------------------------------------------------------------
#Author - Hari Udayakumar h.udayakumar.ee@lantiq.com
#
#Refer INA219 Spec for Detailed Calculation on Current LSB Value
#Note the Current LSB Value choosen is 200e-6
#
#--------------------------------------------------------------------------------
from etc_ftdi_main import *

etc = etc_main()
etc.etc_i2c_init()
etc.etc_config_cal()
etc.etc_rd_all()

		
