#This Python Script is for Emulating I2C Protocol using Asynchronous Bit Bang Mode

import d2xx
import time
import sys

class BB_I2C(object):

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
			
	def I2C_Idle(self):
		self.port.setBitMode(0x60,0x4)
		self.port.write('\xFF')
	
	def I2CStart_CMD(self):
		self.port.write("\xFF")								#SDA and SCK are Pulled High
		time.sleep(0.001)
		self.port.write("\xDF")								#Pull SDA Low
		time.sleep(0.001)
		self.port.write("\x9F")								#Pull SCK and SDA Low
		
		
	def I2CStop_CMD(self):
		self.port.write("\xDF")
		time.sleep(0.001)
		self.port.write("\xFF")
		time.sleep(0.001)
		self.port.write("\x9F")
		
	def SendAddr(self,Addr,RW):
		temp=self.port.getStatus()
		databuf = self.port.read(temp[0])
		dataToSend=self._i2c_str(bin((Addr|RW)|2**32)[-8:])+"\xBF\xFF\xBF"	#Sending Device Address
		dataLen=len(dataToSend)
		self.port.write(dataToSend)
		dataRead = self.port.read(dataLen)			#Reading Acknowledgement
		DataCheck=int(dataRead[dataLen-1].encode('hex'),16) & 0x20
		if DataCheck != 0:
			pass#print("Error SendAddr %x %x- ACK Not Received"%(Addr,RW))
			#print dataRead.encode('hex') #hex(ord(dataRead))
		else:
			pass#print("SendAddr %d - ACK Received"%Addr)
		return dataRead
		
		
	def SendByte(self,data):
		temp=self.port.getStatus()
		databuf = self.port.read(temp[0])
		data = int(data,16) 
		dataToSend=self._i2c_str(bin(data|2**32)[-8:])+"\xBF\xFF\xBF"		#Sending Data - for every bit of actual data - 3 values are transmitted where the clk --goes from 0 to 1 to 0 and data remains constant
		dataLen=len(dataToSend)
		self.port.write(dataToSend)
		dataRead = self.port.read(dataLen)#Reading Acknowledgement
		DataCheck=int(dataRead[dataLen-2].encode('hex'),16) & 0x20
		if DataCheck != 0:
			pass#print("Error SendByte %d - ACK Not Received"%data)
			#print dataRead.encode('hex')#hex(ord(dataRead))
		else:
			pass#print("SendByte %d Received"%data)
		return dataRead
		
	def ReadByteAK(self):
		temp=self.port.getStatus()
		databuf = self.port.read(temp[0])
		dataToSend = self._i2c_str("1"*8+"0")
		dataLen=len(dataToSend)
		self.port.write(dataToSend)
		dataRead = self.port.read(dataLen)
		r=""
		for i in range(8):														#3 Samples of Data Available ---> __:---:___
			r += str(int(dataRead[((i*3)+1)].encode('hex')[0],16)>>1 & 0x1)			# dissecting the MSB value [0] and masking the bit no '4' i.e DI Pin
		return hex(int(r,2))[2:]
			
	def ReadByteNAK(self):
		temp=self.port.getStatus()
		databuf = self.port.read(temp[0])
		dataToSend = self._i2c_str("1"*8+"1")
		dataLen=len(dataToSend)
		self.port.write(dataToSend)
		dataRead = self.port.read(dataLen)
		r=""
		for i in range(8):														#3 Samples of Data Available ---> __:---:___
			r += str(int(dataRead[((i*3)+1)].encode('hex')[0],16)>>1 & 0x1)			# dissecting the MSB value [0] and masking the bit no '4' i.e DI Pin
			
		return hex(int(r,2))[2:]
			
	def _i2c_str(self,a):
		r = ""
		for c in a:
			if c=='0' :
				r = r + "\x9F\xDF\x9F"
			else:
				r = r + "\xBF\xFF\xBF"		
		return r		
				
			