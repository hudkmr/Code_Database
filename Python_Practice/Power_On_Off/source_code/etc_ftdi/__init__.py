import d2xx
import time

class MPSSE_I2C(object):

	dataRBuff=''
	dataTBuff=''
	
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
		
		
	def DevConf_ABB(self,baud,mask,mode):
		self.port.setBaudRate(baud)
		self.port.setBitMode(mask,mode)
	
	def DevConf_I2C(self):
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
		#Configure MPSSE I2C settings
		dataTBuff="8A978D".decode('hex')				#3Phase Clock Enabled
		self.port.write(dataTBuff)
		dataTBuff="800313".decode('hex')
		self.port.write(dataTBuff)
		dataTBuff="86973A".decode('hex')
		self.port.write(dataTBuff)		
		#Turn off Loopback
		self.port.write('\x85')
		time.sleep(5)
		
	def I2CStart_CMD(self):
		#Opcode 0x80 Sets the Lower Byte of MPSSE as Out Port
		#Opcode 0x03 Bit0 - SCK Bit1 - SDA/DO  Bit2-SDA/DI
		#Opcode 0x13 Setting SCK and SDA Pins to 1	
		dataTBuff='800313'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='800103'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='800013'
		self.port.write(dataTBuff.decode('hex'))
	
	def I2CStop_CMD(self):
		dataTBuff='800103'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='800303'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='800003'
		self.port.write(dataTBuff.decode('hex'))
	
	def I2C_Idle(self):
		dataTBuff='800203'
		self.port.write(dataTBuff.decode('hex'))
		
	def SendAddr(self,Addr,RW):
		data=hex(Addr|RW)
		dataTBuff="110000"+data[2:]+"800203220087"
		self.port.write(dataTBuff.decode('hex'))
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = self.port.read(dataToRead)
		DataCheck= int(dataRBuff.encode('hex'),16) & 1
		return DataCheck
				
	def SendByte(self,data):
		dataTBuff="110000"+data+"800203220087"
		self.port.write(dataTBuff.decode('hex'))
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = self.port.read(dataToRead)
		DataCheck= int(dataRBuff.encode('hex'),16) & 1
		return DataCheck
		
	def ReadByteAK(self):
		dataTBuff="200000"+"130000"+"80020387"
		self.port.write(dataTBuff.decode('hex'))	
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = self.port.read(dataToRead)
		return dataRBuff		
	
	def ReadByteNAK(self):
		dataTBuff="200000"+"1300FF"+"80020387"
		self.port.write(dataTBuff.decode('hex'))	
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = self.port.read(dataToRead)
		return dataRBuff

			
	def close(self):
		pass
		
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
		