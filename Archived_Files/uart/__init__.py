#UART Communication using D2xx Library
import d2xx
import time

class UART(object):

	dataRBuff=''
	dataTBuff=''
	
	def __init__(self,port):
		#List of FTDI Devices Available
		devAvail = d2xx.listDevices()
		if not devAvail:
			print("Error - Check your Connection to FTDI Device")
		else:	
			self.port=d2xx.open(port)
			print("Connection to Port %d established"%port)
			
	def Config(self,baud):
		self.port.setBitMode(0,0)							#Resetting MPSSE - Enabling Default UART Mode
		self.port.setBaudRate(baud)							#Configure the Baud Rate
		self.port.setDataCharacteristics(8,1,0)				#UART Set to 8 Bit Mode with 1 Stop Bit and No Parity
		self.port.setFlowControl(0)							#Disabling UART Flow Control
		#print("UART Port Configured for %d Baud Rate"%baud)
		time.sleep(0.1)
		dataToSend = '\x1B\r\n'
		self.port.write(dataToSend)
		dataToRead = 0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRead = self.port.read(dataToRead)
		#print dataRead
		
	def WR(self,data):
		dataToSend = data+'\r\n'
		self.port.write(dataToSend)
		time.sleep(0.1)
		dataToRead = 0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRead = self.port.read(dataToRead)
		
	def RD(self,data):
		dataToSend = data+'\r\n'
		dataLen = len(dataToSend)
		self.port.write(dataToSend)
		time.sleep(0.1)
		dataToRead = 0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRead = self.port.read(dataToRead)
		return dataRead[dataLen:-3]
		
	def Close(self):
		self.port.close()