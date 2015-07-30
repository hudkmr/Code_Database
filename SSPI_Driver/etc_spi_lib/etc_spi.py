#SPI Application
def ETC_Reg_Read_NS(dev,addr,burst_size):
	dataRBuff=[]
	dev.SPI_Write('03')
	dev.SPI_Write(addr[0:2])
	dev.SPI_Write(addr[2:])
	dev.SPI_Write(burst_size)
	dataRBuff+=dev.SPI_Read()
	dataRBuff+=dev.SPI_Read()
	return dataRBuff
	
def ETC_Reg_Read_AS(dev,addr,burst_size):
	dataRBuff=[]
	dev.SPI_Write('2B')
	dev.SPI_Write(addr[0:2])
	dev.SPI_Write(addr[2:])
	dev.SPI_Write(burst_size)
	dataRBuff+=dev.SPI_Read()
	return dataRBuff
	
def ETC_Reg_Write_NS(dev,addr,data):
	dev.SPI_Write('02')
	dev.SPI_Write(addr[0:2])
	dev.SPI_Write(addr[2:])
	dev.SPI_Write(data[0:2])
	dev.SPI_Write(data[2:])
		
	
def ETC_Reg_Write_AS(dev,addr,data):
	dev.SPI_Write('2A')
	dev.SPI_Write(addr[0:2])
	dev.SPI_Write(addr[2:])
	dev.SPI_Write(data[0:2])
	dev.SPI_Write(data[2:])
		

#Baudrate Calculation
#SK frequency = 60MHz /((1 + [(1 +0xValueH*256) OR 0xValueL])*2)
#BaudRate = (60MHz /( 2* SPI_CLK)) - 1	
def BaudRate(spi_clk):
		baudrate = hex(int((60e3/(2*spi_clk)) -1))[2:]
		while len(baudrate) < 4:
			baudrate = '0' + baudrate
		baudrate = baudrate[2:]+baudrate[0:2]
		return baudrate
		