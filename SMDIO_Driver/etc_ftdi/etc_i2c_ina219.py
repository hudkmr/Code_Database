#This Script Reads the Data from I2C Slave device(Flash memory) using FTDI MPSSE Engine
#DataReception
def INA219_Reg_RRead(d,SlaveAddr,Reg,RW):
	Noerror = 1
	while Noerror:
		RXData=""
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,RW[0])
		Noerror = d.SendByte(Reg)
		d.I2CStart_CMD()
		Noerror =d.SendAddr(SlaveAddr,RW[1])
		RXData+=d.ReadByteAK()	
		RXData+=d.ReadByteNAK()
		d.I2CStop_CMD()
	return RXData
	
def INA219_Reg_Write(d,SlaveAddr,Reg,Data,RW):
	Noerror =1
	while Noerror:
		d.I2CStart_CMD()
		Noerror = d.SendAddr(SlaveAddr,RW[0])	
		Noerror = d.SendByte(Reg)
		Noerror = d.SendByte(Data[0:2])					#'1000' - 10 is Msb which is [0:2]
		Noerror = d.SendByte(Data[2:])					#       - 00 is Lsb which is [2:]
		d.I2CStop_CMD()
	return Noerror
	





	

