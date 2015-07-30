#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
#DataReception
def INA219_Reg_RRead(d,SlaveAddr,Reg,RW):
	RXACKBuf=[]
	RXData=""
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(SlaveAddr,RW[0])
	RXACKBuf+=d.SendByte(Reg)
	d.I2CStart_CMD()
	RXACKBuf+=d.SendAddr(SlaveAddr,RW[1])
	RXData+=d.ReadByteAK()	
	RXData+=d.ReadByteNAK()
	d.I2CStop_CMD()
	return RXData	

#Data Transmission	
def INA219_Reg_Write(d,SlaveAddr,Reg,Data,RW):
	TXACKBuf=[]
	d.I2CStart_CMD()
	TXACKBuf+=d.SendAddr(SlaveAddr,RW[0])	
	TXACKBuf+=d.SendByte(Reg)
	TXACKBuf+=d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
	TXACKBuf+=d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
	d.I2CStop_CMD()
	return TXACKBuf	

