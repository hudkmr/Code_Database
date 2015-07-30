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
	
	def DevConf_SMM(self):
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
				print("MPSSE - Synchronize and Ready of Data Transaction!")
			dataToRead=self.port.getQueueStatus()
		#Configure MPSSE I2C settings
		dataTBuff="8A978C".decode('hex')
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
		dataTBuff='80FDFB'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='80FCFB'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='82BF40'
		self.port.write(dataTBuff.decode('hex'))
	
	def I2CStop_CMD(self):
		dataTBuff='80FCFB'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='80FDFB'
		for i in range(4):
			self.port.write(dataTBuff.decode('hex'))
		dataTBuff='80FFFB'
		self.port.write(dataTBuff.decode('hex'))

		
	def SendByte(self,datalen,data):
		dataTBuff="11"+str(datalen[2:])+str(datalen[0:2])+data+"80FEFB220087"
		self.port.write(dataTBuff.decode('hex'))
		#time.sleep(0.1)
		#dataToRead = self.port.getQueueStatus()
		#while dataToRead:
		#	dataRBuff = str(self.port.read(dataToRead))
		#	dataToRead = self.port.getQueueStatus()
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		dataRBuff = str(self.port.read(dataToRead))
		if dataRBuff != '\x00':
			print("Error - ACK Not Recevied")
		#else:
			#print("ACK Received")
		return dataRBuff

	def ReadByteAK(self,datalen):
		dataTBuff="80001124"+str(datalen[2:])+str(datalen[0:2])+"0000120187"
		self.port.write(dataTBuff.decode('hex'))	
		#time.sleep(0.1)
		#dataToRead = self.port.getQueueStatus()
		#while dataToRead:
		#	dataRBuff = str(self.port.read(dataToRead))
		#	dataToRead = self.port.getQueueStatus()
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		print dataToRead	
		dataRBuff = self.port.read(dataToRead)
		dataRBuff
		return dataRBuff		
	
	def ReadByteNAK(self):
		dataTBuff="80001124000012FF87".decode('hex')
		self.port.write(dataTBuff)	
		#time.sleep(0.1)
		#dataToRead = self.port.getQueueStatus()
		#while dataToRead:
		#	dataRBuff = str(self.port.read(dataToRead))
		#	dataToRead = self.port.getQueueStatus()
		dataToRead=0
		while not dataToRead:
			dataToRead = self.port.getQueueStatus()
		print dataToRead	
		dataRBuff = self.port.read(dataToRead)
		dataRBuff
		return dataRBuff

			
	def close(self):
		pass
		