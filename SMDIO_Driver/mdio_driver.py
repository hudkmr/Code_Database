#MDIO Driver File
from etc_mdio_lib import *
from etc_mdio_lib.etc_mdio_header import *
from etc_uart import *
import shlex

dev=BB_MDIO(0)
dev.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)

print "Enter the command to write or read SMDIO Interface"
print "For reading command format - r \"addr\" \"offset\""
print "For writing command format - w \"addr\" \"offset\" \"data\""
print "For exiting command format - quit"

if HALT_MODE == False:
	uart=uart_reg_rw(1,921600)
	#Enabling MDIO Interface
	uart.gphy_wr('fa01','0000')
	uart.gphy_wr('f383','03c3')
	uart.gphy_wr('f384','003f')
	uart.gphy_wr('f480','01f1')
else:	
	while loop == True:
		input = raw_input()
		command = shlex.split(input)
		if command[0] == 'quit':
			loop = False
		elif command[0] == 'r':
			addr = int(command[1],16)
			offset = int(command[2],16)
			data = etc_pdi_read(dev,addr,offset)
			print data
		elif command[0] == 'w':
			addr = int(command[1],16)
			offset = int(command[2],16)
			dataw = int(command[3],16)
			etc_pdi_write(dev,addr,offset,dataw)
	