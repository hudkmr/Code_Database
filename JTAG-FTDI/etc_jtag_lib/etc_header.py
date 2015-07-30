#This Header file consists of the Global variable used in SPI Communication
jtag_clk = 100000

#Baudrate Calculation
#SK frequency = 60MHz /((1 + [(1 +0xValueH*256) OR 0xValueL])*2)
#BaudRate = (60MHz /( 2* SPI_CLK)) - 1	
def BaudRate(spi_clk):
		baudrate = hex(int((60e3/(2*spi_clk)) -1))[2:]
		while len(baudrate) < 4:
			baudrate = '0' + baudrate
		baudrate = baudrate[2:]+baudrate[0:2]
		return baudrate
