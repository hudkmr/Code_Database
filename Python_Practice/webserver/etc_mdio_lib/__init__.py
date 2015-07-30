#This Python Script is for Emulating I2C Protocol using Asynchronous Bit Bang Mode(PortA1 -- PortA8)
#PortA.6 == CLK
#PortA.7 == Data


import d2xx
import time
import sys

class BB_MDIO(object):

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
			
	def DevConf(self,baud,mask,mode):
		self.port.setBaudRate(baud)
		self.port.setBitMode(mask,mode)
		self.port.write('\xFF')		
			
	def MDIO_Write(self,Phy,Reg,Data):
		Phy  = self._mdio_dc(5,Phy)
		Reg  = self._mdio_dc(5,Reg)
		Data = self._mdio_dc(16,Data)
		dataBuf=''
		#32 Consecutive One's for MDIO Synchronisation
		for i in range(32):
			dataBuf += '1'
		#Start Code and Opcode
		dataBuf += '0101' + Phy + Reg + '10'+ Data
		#Phyaddr and Reg
		dataToSend = self._mdio_str(dataBuf)
		self.port.write(dataToSend)
		
	def MDIO_Read(self,Phy,Reg):
		Phy  = self._mdio_dc(5,Phy)
		Reg  = self._mdio_dc(5,Reg)
		Data = self._mdio_dc(16,0xFFFF)
		dataBuf=''
		#32 Consecutive One's for MDIO Synchronisation
		for i in range(32):
			dataBuf += '1'
		#Start Code and Opcode
		dataBuf += '0110' + Phy + Reg + '10'+ Data
		#Phyaddr and Reg
		dataToSend = self._mdio_str(dataBuf)
		dataLen=len(dataToSend) 
		offset = dataLen - len(self._mdio_str(Data))
		self.port.write(dataToSend)	
		dataRBuf = self.port.read(dataLen)
		print dataRBuf
		dataRead=[]
		for i in range(offset,dataLen):
			dataRead += dataRBuf[i].encode('hex'),
		return dataRead
		
	def _mdio_dc(self,width,a):
		r=""
		for i in range(width):
			if (a>>((width-1)-i) & 1) == 0:
				r += '0'
			else:
				r += '1'
		return r		
		
	def _mdio_str(self,a):
		r = ""
		for c in a:
			if c=='0' :
				r = r + "\x9F\xDF\x9F"
			else:
				r = r + "\xBF\xFF\xBF"		
		return r		
				
			