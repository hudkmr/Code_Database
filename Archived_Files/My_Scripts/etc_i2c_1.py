from etc_ftdi import MPSSE_I2C
import time

d=MPSSE_I2C(0)
d.DevConf_SMM()
d.I2CStart_CMD()
data=d.SendByte('0000','89') 
#time.sleep(0.1)
data=d.ReadByteAK()
#data=d.ReadByteNAK()