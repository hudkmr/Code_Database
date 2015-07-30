from etc_spi_lib import MPSSE_SPI
from etc_spi_lib.etc_spi import BaudRate
from etc_spi_lib.ftdi_spi_msp25pe10vp_lib  import *
from etc_spi_lib.ftdi_spi_msp25pe10vp_header import *
import time

spi_clk=5000
baudrate=BaudRate(spi_clk)	
dev=MPSSE_SPI(0)
dev.DevConf(baudrate)

#Read Identification Register
dev.SPI_CS_Enable()
dataRead=Read_Identification(dev)
dataRead_F=[]
for i in range(len(dataRead)):
	print dataRead[i].encode('hex')

#Write and Read 8 Bytes of Data to 
Page_Write_Enable(dev)
dataRead=Read_Status_Reg(dev)
Page_Program(dev,Waddr,Wdata)
dataRead=[]
dataRead=Page_Read(dev,Raddr,Rsize)
print dataRead

