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
		dataTBuff="8A978C".decode('hex')				#3Phase Clock Disabled
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
		dataTBuff='800313'
		self.port.write(dataTBuff.decode('hex'))
		
	def SendAddr(self,Addr,RW):
		data=hex(Addr|RW)
		print data[2:]
		dataTBuff="110000"+data[2:]+"220087"
		self.port.write(dataTBuff.decode('hex'))
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = str(self.port.read(dataToRead))
		if dataRBuff != '\x00':
			#print dataRBuff.encode('hex')
			print("Error SendAddr - ACK Not Recevied")

		return dataRBuff
		
	def SendByte(self,data):
		dataTBuff="110000"+data+"220087"
		self.port.write(dataTBuff.decode('hex'))
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = str(self.port.read(dataToRead))
		if dataRBuff != '\x00':
			#print dataRBuff.encode('hex')
			print("Error SendByte - ACK Not Received")
		return dataRBuff

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
		