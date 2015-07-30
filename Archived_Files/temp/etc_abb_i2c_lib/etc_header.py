#This Script Contains List of Variable used in I2C Read Write Functions

SYNC_MODE=0x4
DO_MASK_VAL=0x60
DI_MASK_VAL=0x40
PORT_INT=00
BAUD=300
WR=0
RD=1
SlaveAddr=0x8E
I2C_ADDR = [0x40,0x41,0x43,0x44,0x45,0x47]
CAL_VAL  = ['9174','9174','ADE9','9174','9174','ADE9']
CUR_LSB  = [0.11,0.11,0.092,0.11,0.11,0.092]
PWR_LSB  = [2.2,2.2,1.84,2.2,2.2,1.84]
FLD_ADDR = [0x50,0x53]
TPS_ADDR = [0x60,0x61]
TPS_REG  = ['01',]
Error_Message=True
INA219_REG=['00','01','02','03','04','05']
#INA219_REG=[0,1,2,3,4,5]
