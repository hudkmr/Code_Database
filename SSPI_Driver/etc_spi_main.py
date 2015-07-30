#Main Script File - SPI Slave Mode Read Write Operation
from etc_spi_lib 			import MPSSE_SPI
from etc_spi_lib.etc_spi 	import *
from etc_spi_lib.etc_header import *

import time
import sys

'''

print("To Read  enter the \'r\' command and addr      exp - r fa01")
print("To Write enter the \'w\' command and addr/data exp - w fa01 0000")
print("To Quit  enter the \'x\' command")
spi_clk = 2500
'''

spi_clk = int(raw_input("Enter SPI Clk Frequency (KHz):"))
if spi_clk >= 2500:
	Mode = SPI_AUTO_SYNC_MODE
else:
	Mode = SPI_NON_SYNC_MODE

baudrate=BaudRate(spi_clk)	
dev=MPSSE_SPI(0)
dev.DevConf(baudrate)	
while True:
	command=raw_input("Enter the Cmd to Read/Write a Register:")
	if command[0] is 'x':
		break
	elif  not (command[0] == 'r' or command[0] == 'w'):
		print("Enter Proper Command")
	else: 
		addr = command[2:6]
		if command[0] is 'r':
			if Mode == SPI_AUTO_SYNC_MODE:
				dataRead=ETC_Reg_Read_AS(dev,addr,BURST_SIZE)
				print dataRead
			else:
				dataRead=ETC_Reg_Read_NS(dev,addr,BURST_SIZE)
				print dataRead
		elif command[0] is 'w':
			data = command[7:11]
			if Mode == SPI_AUTO_SYNC_MODE:
				dataSent=ETC_Reg_Write_AS(dev,addr,data)
			else:
				dataSent=ETC_Reg_Write_NS(dev,addr,data)
				
			
		
		
