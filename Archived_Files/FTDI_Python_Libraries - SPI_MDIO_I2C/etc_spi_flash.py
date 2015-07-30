from etc_spi_lib 			import MPSSE_SPI
from etc_spi_lib.etc_spi  	import *
import time

def Page_Write_Enable():
	dataToSend='06'
	dataLen='0000'
	dev.SPI_Write(dataLen,dataToSend)
	
def Page_Write_Disable():
	dataToSend='04'
	dataLen='0000'
	dev.SPI_Write(dataLen,dataToSend)	
	
def Page_Write(addr,data):
	dataToSend='02'
	dataToSend+=addr
	dataToSend+=data
	dataLen=hex(len(dataToSend)/2 - 1)[2:]
	while len(dataLen) < 4:
		dataLen = '0' + dataLen
	dev.SPI_Write(dataLen,dataToSend)
	
	
def Page_Read(addr):
	dataRBuff=[]
	dataToSend='03'
	dataToSend+= addr
	dataLen=hex(len(dataToSend)/2 - 1)[2:]
	while len(dataLen) < 4:
		dataLen = '0' + dataLen
	dev.SPI_RWrite(dataLen,dataToSend)	
	dataRBuff+=dev.SPI_Read('000F')
	return dataRBuff
	
def Read_Status_Reg():
	dataRBuff=[]
	dataToSend='05'
	dataLen='0000'
	dev.SPI_RWrite(dataLen,dataToSend)
	dataRBuff+=dev.SPI_Read('0001')
	return dataRBuff

def Read_Identification():
	dataRBuff=[]
	dataToSend='9F'								#Read Command
	dataLen='0000'
	dev.SPI_Write(dataLen,dataToSend)
	dataRBuff+=dev.SPI_Read('000F')
	return dataRBuff	
	
spi_clk=300
baudrate=BaudRate(spi_clk)	
dev=MPSSE_SPI(0)
'''
dev.DevConf(baudrate)
time.sleep(0.1)
dataRead = Read_Identification()
print dataRead


Waddr='000100'
Wdata='0102030405060708'
Page_Write_Enable()
Page_Write(Waddr,Wdata)
dataRead=Read_Status_Reg()
print dataRead
dataRead=Page_Read(Waddr)



time.sleep(0.1)
Page_Write_Disable()
dataRead=Page_Read(Waddr)
print dataRead
dataRead=Read_Identification()
for i in range(len(dataRead)):
	print dataRead[i].encode('hex')
#dataRead=Read_Status_Reg()
#print dataRead
Waddr='000100'
Wdata='0102030405060708'
Page_Write_Enable()
Page_Write(Waddr,Wdata)
time.sleep(0.1)
Page_Write_Disable()
dataRead=Page_Read(Waddr)
print dataRead
'''