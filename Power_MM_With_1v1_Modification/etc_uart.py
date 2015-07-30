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
