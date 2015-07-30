#SPI Application
def ETC_Reg_Read_NS(dev,addr,burst_size):
	dataToSend=""
	dataToSend+='03'								#Read Command
	dataToSend+=addr
	dataToSend+=burst_size
	dataLen=hex(len(dataToSend)/2 -1)[2:]
	while len(dataLen) < 4:
			dataLen = '0' + dataLen
	dev.SPI_RWrite(dataLen,dataToSend)
	dataRBuff=dev.SPI_Read('0001')
	return dataRBuff

def ETC_Reg_Read_AS(dev,addr,burst_size):
	dataToSend=""
	dataToSend+='2B'								#Read Command
	dataToSend+=addr
	dataToSend+=burst_size
	dataLen=hex(len(dataToSend)/2 -1)[2:]
	while len(dataLen) < 4:
			dataLen = '0' + dataLen
	dev.SPI_RWrite(dataLen,dataToSend)
	dataRBuff=dev.SPI_Read('0001')
	return dataRBuff
	
def ETC_Reg_Write_NS(dev,addr,data):
	dataToSend=""
	dataToSend+='02'
	dataToSend+=addr
	dataToSend+=data
	dataLen=hex(len(dataToSend)/2 -1)[2:]
	while len(dataLen) < 4:
			dataLen = '0' + dataLen
	dev.SPI_Write(dataLen,dataToSend)
	
def ETC_Reg_Write_AS(dev,addr,data):
	dataToSend=""
	dataToSend+='2A'
	dataToSend+=addr
	dataToSend+=data
	dataLen=hex(len(dataToSend)/2 -1)[2:]
	while len(dataLen) < 4:
			dataLen = '0' + dataLen
	dev.SPI_Write(dataLen,dataToSend)
	
