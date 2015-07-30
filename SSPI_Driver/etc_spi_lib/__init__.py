#This Driver Configure the FTDI Device with SPI Functionality using MPSSE Mode
import d2xx
import sys
import time

class MPSSE_SPI(object):
	
	def __init__(self,port):
		#List of FTDI Devices Available
		devAvail = d2xx.listDevices()
		if not devAvail:
			print("Error - Check your Connection to FTDI Device")
		else:	
			self.port=d2xx.open(port)
			self.port.resetDevice()
			dataToRead=self.port.getQueueStatus()
			while dataToRead:
				dataRBuff=self.port.read(dataToRead)
				dataToRead=self.port.getQueueStatus()
			print("Connection to Port %d established"%port)
			
	def DevConf(self,baudrate):
		self.port.setUSBParameters(65536,65535)					#USB request Transfer size
		self.port.setChars('0',0,'0',0)							#Disable Event and error characters
		self.port.setTimeouts(0,5000)
		self.port.setLatencyTimer(16)
		self.port.setBitMode(0,0)								#reset Controller
		self.port.setBitMode(0,2)								#MPSSE Mode Enable
		
		#MPSSE Synchornisation and Receiving Back Bad Commands
		dataTBuff = 'AA'.decode('hex')
		self.port.write(dataTBuff)
		time.sleep(0.1)
		dataToRead=self.port.getQueueStatus()
		while dataToRead:
			dataRBuff=self.port.read(dataToRead)
			if dataRBuff[0] != '\xFA' and dataRBuff[1] != '\xAA':
				print("Error - MPSSE is not Synchronized!")
			else:
				print("MPSSE - Synchronized and Ready of Data Transaction!")
			dataToRead=self.port.getQueueStatus()
			
		#Configure the MPSSE for SPI communication
		#Configure MPSSE I2C settings
		dataTBuff="8A978D".decode('hex')				#3Phase Clock Disabled
		self.port.write(dataTBuff)
		dataTBuff="80000B".decode('hex')
		self.port.write(dataTBuff)
		dataTBuff=("86"+baudrate).decode('hex')
		self.port.write(dataTBuff)		
		#Turn off Loopback
		self.port.write('\x85')
		time.sleep(5)
		
	def SPI_CS_Enable(self):
		dataTBuff='80080B'
		for i in range(5):
			self.port.write(dataTBuff.decode('hex'))
	
	def SPI_CS_Disable(self):
		dataTBuff='80080B'
		for i in range(5):
			self.port.write(dataTBuff.decode('hex'))	
			
	def SPI_Write(self,data):
		dataTBuff = "80000B110000"+data+"80080B"
		self.port.write(dataTBuff.decode('hex'))
						
	def SPI_Read(self):
		dataTBuff = "80000B24010080080B"
		self.port.write(dataTBuff.decode('hex'))
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = self.port.read(dataToRead)
		return dataRBuff
		
		
			