#This Python File Consits of List of SPI Commands Related MSP25PE10 Flash Memory
def Page_Write_Enable(dev):
	dataToSend='06'
	dataLen='0000'
	dev.SPI_Write(dataLen,dataToSend)
	
def Page_Write_Disable(dev):
	dataToSend='04'
	dataLen='0000'
	dev.SPI_Write(dataLen,dataToSend)	
	
def Page_Program(dev,addr,data):
	dataToSend='02'
	dataToSend+=addr
	dataToSend+=data
	dataLen=hex(len(dataToSend)/2 - 1)[2:]
	while len(dataLen) < 4:
		dataLen = '0' + dataLen
	dev.SPI_Write(dataLen,dataToSend)
	
	
def Page_Read(dev,addr,size):
	dataRBuff=[]
	dataToSend='03'
	dataToSend+= addr
	dataLen=hex(len(dataToSend)/2 - 1)[2:]
	while len(dataLen) < 4:
		dataLen = '0' + dataLen
	dev.SPI_RWrite(dataLen,dataToSend)	
	dataRBuff+=dev.SPI_Read(size)
	return dataRBuff
'''	
def Read_Status_Reg(dev):
	dataRBuff=[]
	dataToSend='05'
	dataLen='0000'
	dev.SPI_RWrite(dataLen,dataToSend)
	dataRBuff+=dev.SPI_Read('0001')
	return dataRBuff
'''

def Read_Identification(dev):
	dataRBuff=[]
	dataToSend='9F'	
	dataLen = '000F'	
	dataRBuff+= dev.SPI_RW(dataLen,dataToSend)
	return dataRBuff	
	


