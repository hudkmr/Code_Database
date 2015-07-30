from etc_ftdi import UART

MDIO_RD = 2
MDIO_WR = 1


class uart_reg_rw():
	def __init__(self,port,baud):
		self.d = UART(port)
		self.d.Config(baud)
		
	def gphy_rd(self,reg):
		command = 'r ' + reg
		output = self.d.RD(command)
		return output
		
	def gphy_wr(self,reg,data):
		command = 'w '+ reg + ' ' + data
		self.d.WR(command)
		
	def gphy_close(self):
		self.d.Close()

def mdio_read(uart,phy,reg):
			command = hex(MDIO_RD << 10 | phy << 5 | reg)[2:]
			if len(command) < 4:
				command = '0' + command		
			uart.gphy_wr('f408',command)	
			dataRead = uart.gphy_rd('f409')
			return dataRead
			
def mdio_write(uart,phy,reg,data):
			command = hex(MDIO_WR << 10 | phy << 5 | reg)[2:]
			data = hex(data)[2:]
			if len(command) < 4:
				command = '0' + command
			if len(data) < 4:
				data = '0' + data		
			uart.gphy_wr('f40a',data)
			uart.gphy_wr('f408',command)				

def gphy_enable(uart):
	output = uart.gphy_rd('fa01')
	if output is not '0000':
		uart.gphy_wr('fa01','0000')
		output = uart.gphy_rd('fa01')
		print('GPHY addr FA01 - %s'%output)

def etc_master_enable(uart):
	for i in range(5):
		print mdio_read(uart,i,9)
	for i in range(5):
		mdio_write(uart,i,9,0x1b00)
	for i in range(5):
		print mdio_read(uart,i,9)	
	
def etc_slave_enable(uart):
	for i in range(5):
		print mdio_read(uart,i,9)
	for i in range(5):
		mdio_write(uart,i,9,0x0300)
	for i in range(5):
		print mdio_read(uart,i,9)	
				
def etc_fetl(uart):
	print('Started - Configuring ETC for FETL Mode')
	uart.gphy_wr('fa01','0000')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','0413')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','0400')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','0433')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','0420')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','0453')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','0440')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','0473')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','0460')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','0493')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','0480')
	uart.gphy_wr('f40a','4003')
	uart.gphy_wr('f408','04B3')
	uart.gphy_wr('f40a','1200')
	
	uart.gphy_wr('f408','04A0')
	print('Finished - Configuring ETC for FETL Mode')
	
def etc_jumbo(uart):
		print('Configure - Jumbo Packet Testing for ETC')
		uart.gphy_wr('ed05','000d')
		uart.gphy_wr('e911','000d')
		uart.gphy_wr('e91d','000d')
		uart.gphy_wr('e929','000d')
		uart.gphy_wr('e935','000d')
		uart.gphy_wr('e941','000d')
		uart.gphy_wr('e94d','000d')
		
def Link_1000mb(uart):
	print('setting gphy port to 1G Mode')
	uart.gphy_wr('fa01','0000')
	for i in range(6):
		mdio_write(uart,i,9,0x0200)
		mdio_write(uart,i,4,0x01E1)
		mdio_write(uart,i,0,0x1200)

def Link_100mb(uart):
	print('setting gphy port to 100MB Mode')
	uart.gphy_wr('fa01','0000')
	for i in range(6):
		mdio_write(uart,i,9,0x0000)
		mdio_write(uart,i,4,0x0201)
		mdio_write(uart,i,0,0x1200)

def Link_10mb(uart):
	print('setting gphy port to 10M Mode')
	uart.gphy_wr('fa01','0000')
	for i in range(6):
		mdio_write(uart,i,9,0x0000)
		mdio_write(uart,i,4,0x0021)
		mdio_write(uart,i,0,0x1200)

def set_gphy_link(uart,link_speed):
	if link_speed == '1000':
		Link_1000mb(uart)
	elif link_speed == '100':
		Link_100mb(uart)
	elif link_speed == '10':
		Link_10mb(uart)
		