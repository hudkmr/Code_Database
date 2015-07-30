#This Function enables MPSSE Mode and Initializes FTDI Device

from etc_ftdi 				import MPSSE_I2C
from etc_ftdi.etc_header 	import *
from etc_ftdi.etc_i2c_cmds 	import *

d=MPSSE_I2C(0)
d.DevConf_I2C()
data =INA219_Reg_RRead(d,(I2C_ADDR[0]<<1),INA219_REG[1])
print data