from etc_ftdi import UART

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

def gphy_enable(uart):
	output = uart.gphy_rd('fa01')
	if output is not '0000':
		uart.gphy_wr('fa01','0000')
		output = uart.gphy_rd('fa01')
		print('GPHY addr FA01 - %s'%output)
		
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
	
