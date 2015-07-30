#This Driver Configure the FTDI Device with SPI Functionality using MPSSE Mode
import d2xx
import sys
import time

class MPSSE_JTAG(object):
	
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
		dataTBuff="8A978D".decode('hex')				#1.Use 60Mhz Clock, 2.Turn off adaptive Clocking, 3. 3Phase Clock Disabled
		self.port.write(dataTBuff)
		dataTBuff="80080B".decode('hex')				#Initialize and Direction config
		self.port.write(dataTBuff)
		#dataTBuff="820000".decode('hex')				#Initialize and Direction config
		#self.port.write(dataTBuff)
		dataTBuff=("86"+baudrate).decode('hex')			
		self.port.write(dataTBuff)		
		#Turn off Loopback
		self.port.write('\x85')
		time.sleep(5)
		
	def JTAG_Test_Logic_Reset_State(self):
		dataTBuff='4B07FF'.decode('hex')
		self.port.write(dataTBuff)
		print('JTAG Is Test Logic Reset State')		
		
	def JTAG_IR_SCAN(self,length,opcode):
		dataTBuff='4B0301'.decode('hex')				#Moving to Shift-IR State
		self.port.write(dataTBuff)
		dataTBuff='3B'
		dataTBuff+=length
		dataTBuff+=opcode						#Load Data 0x04 to IR Register
		self.port.write(dataTBuff.decode('hex'))
		dataTBuff='4B0403'.decode('hex')				#Moving to Move to Exit-IR,Update-IR and RTI State
		self.port.write(dataTBuff)
		
	def JTAG_DR_SCAN(self,length,opcode):
		dataTBuff='4B0406'.decode('hex')				#Moving to Shift-IR State
		self.port.write(dataTBuff)
		dataTBuff='3B'
		dataTBuff+=length
		dataTBuff+=opcode								#Load Data 0x04 to DR Register
		self.port.write(dataTBuff.decode('hex'))
		#dataTBuff='4B0403'.decode('hex')				#Moving to Move to Exit-IR,Update-IR and RTI State
		#self.port.write(dataTBuff)
		
	def JTAG_Shit_IR_State(self):
		dataTBuff='4B050D'.decode('hex')
		self.port.write(dataTBuff)
		print('JTAG Is Shift IR State')	
		
	def JTAG_Shift_Data_IN(self,size,data):
		dataTBuff='3B'
		dataTBuff+=hex(size-1)[:2]
		dataTBuff+=hex(data)[:2]
		self.port.write(dataTBuff.decode('hex'))
		print('Shift Data In')	
		
		
		