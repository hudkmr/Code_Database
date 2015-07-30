#MDIO Driver File
#USE Little Endian Memory
from etc_mdio_lib import *
from etc_mdio_lib.etc_mdio_header import *
from etc_mdio_lib.etc_mdio_func import *
from etc_uart import *
import time

uart_dev=uart_reg_rw(1,115200)

#reading the hex file
file_name = raw_input('Enter the file name:')
hex_file = open(file_name,'r+')
noce = file_len(file_name)
ix = noce
ADDR = int(UART_ADDR,16)

#write the data into SSB Memory
while ix:
#	#Data read from the hex file
	addrS = no_to_str(ADDR)
	dataS = hex_file.read(5)[:-1]
	uart_switch_ssb_write(uart_dev,addrS,dataS)
	dataR = uart_switch_ssb_read(uart_dev,addrS)
	print addrS,hex(ix),dataS,dataR
	ADDR = ADDR - 1
	ix = ix -1


#reduce number of ssb segments to be used by switch
print no_to_str(510-(noce >> 7))
uart_switch_ssb_write(uart_dev,UART_BM_FSQM_GCTRL, no_to_str(510-(noce >> 7)))
uart_switch_ssb_write(uart_dev,UART_BM_GCTRL,'E049')	

#point GPHY CPU' to begining of SSB
uart_dev.gphy_wr(UART_RST_REQ,'101F')
uart_dev.gphy_wr(UART_GPHY_FCR_0,'2000')	
uart_dev.gphy_wr(UART_GPHY_FCR_1,'2000')	
uart_dev.gphy_wr(UART_GPHY_FCR_2,'2000')	
uart_dev.gphy_wr(UART_GPHY_FCR_3,'2000')	
uart_dev.gphy_wr(UART_GPHY_FCR_4,'2000')	
uart_dev.gphy_wr(UART_RST_REQ,'001E')
