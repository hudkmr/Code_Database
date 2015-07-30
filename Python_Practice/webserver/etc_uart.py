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
	
	def gphy_md(self,reg,data,mask):
		command = 'm '+reg+' ' +data+ ' ' +mask
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
	
def packet_ext_enable(uart):
	uart.gphy_wr('fa01','0000')
	uart.gphy_md('fa01','0000','001f')
	uart.gphy_md('fa01','0000','001f')
	uart.gphy_md('f400','8000','FF00')
	uart.gphy_md('F40F','3200','FF00')
	uart.gphy_md('E080','0001','0001')
	uart.gphy_md('E082','0001','0001')
	uart.gphy_md('E084','0001','0001')
	uart.gphy_md('E086','0001','0001')
	uart.gphy_md('E088','0001','0001')
	uart.gphy_md('E08A','0001','0001')
	uart.gphy_md('E08C','0001','0001')
	uart.gphy_md('F130','0200','0200')
	uart.gphy_wr('E455','007f')
	uart.gphy_wr('E454','007f')

def packet_ext_read(uart):
		return uart.gphy_rd('f141')
		
def packet_enable_flush(uart):
	uart.gphy_md('f142','0001','0001')
	
	
def packet_ins_enable(uart):
	uart.gphy_md('fa01','0000','001f')   # release All Gphys
	uart.gphy_md('f400','8000','FF00')   # enable Port 6 and others
	uart.gphy_md('F40F','3200','FF00')   # force 1 G ; link up 
	uart.gphy_md('E080','0001','0001')   # enable RMONS for all ports
	uart.gphy_md('E082','0001','0001')
	uart.gphy_md('E084','0001','0001')
	uart.gphy_md('E086','0001','0001')
	uart.gphy_md('E088','0001','0001')
	uart.gphy_md('E08A','0001','0001')
	uart.gphy_md('E08C','0001','0001')
	uart.gphy_md('F130','0200','0200')   # enable pkt extractor
	
def packet_IPG(uart):
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	uart.gphy_wr('f140','8000')
	
def packet_start(uart):
	#start','Packet
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','81d5')
	uart.gphy_wr('f140','81f4')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','81da')
	uart.gphy_wr('f140','815b')
	uart.gphy_wr('f140','8120')
	uart.gphy_wr('f140','8131')
	uart.gphy_wr('f140','81be')
	uart.gphy_wr('f140','81a1')
	uart.gphy_wr('f140','8179')
	uart.gphy_wr('f140','811c')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','81d9')
	uart.gphy_wr('f140','8186')
	uart.gphy_wr('f140','81dd')
	uart.gphy_wr('f140','816d')
	uart.gphy_wr('f140','815d')
	uart.gphy_wr('f140','81f8')
	uart.gphy_wr('f140','818c')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8112')
	uart.gphy_wr('f140','813c')
	uart.gphy_wr('f140','8113')
	uart.gphy_wr('f140','813d')
	uart.gphy_wr('f140','81a5')
	uart.gphy_wr('f140','811d')
	uart.gphy_wr('f140','8173')
	uart.gphy_wr('f140','813a')
	uart.gphy_wr('f140','8117')
	uart.gphy_wr('f140','8135')
	uart.gphy_wr('f140','815a')
	uart.gphy_wr('f140','81bf')
	uart.gphy_wr('f140','8191')
	uart.gphy_wr('f140','81ae')
	uart.gphy_wr('f140','81bc')
	uart.gphy_wr('f140','8160')
	uart.gphy_wr('f140','81aa')
	uart.gphy_wr('f140','81bf')
	uart.gphy_wr('f140','81c0')
	uart.gphy_wr('f140','8198')
	uart.gphy_wr('f140','81ce')
	uart.gphy_wr('f140','81e0')
	uart.gphy_wr('f140','818d')
	uart.gphy_wr('f140','8148')
	uart.gphy_wr('f140','816b')
	uart.gphy_wr('f140','81e1')
	uart.gphy_wr('f140','8157')
	uart.gphy_wr('f140','81a7')
	uart.gphy_wr('f140','8198')
	uart.gphy_wr('f140','81ea')
	uart.gphy_wr('f140','8177')
	uart.gphy_wr('f140','8122')
	uart.gphy_wr('f140','81bc')
	uart.gphy_wr('f140','8148')
	uart.gphy_wr('f140','81b5')
	uart.gphy_wr('f140','8102')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8157')
	uart.gphy_wr('f140','811b')
	uart.gphy_wr('f140','812d')
	uart.gphy_wr('f140','8102')
	uart.gphy_wr('f140','81a6')
	uart.gphy_wr('f140','810d')
	uart.gphy_wr('f140','8172')
	uart.gphy_wr('f140','81ee')
	uart.gphy_wr('f140','81be')
	uart.gphy_wr('f140','81a1')
	uart.gphy_wr('f140','810d')
	uart.gphy_wr('f140','811e')
	uart.gphy_wr('f140','8131')
	uart.gphy_wr('f140','81fd')
	uart.gphy_wr('f140','8145')
	uart.gphy_wr('f140','81e8')
	uart.gphy_wr('f140','819e')
	uart.gphy_wr('f140','811b')
	uart.gphy_wr('f140','81ae')
	uart.gphy_wr('f140','8131')

def packet_arp(uart):
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','8155')
	uart.gphy_wr('f140','81d5')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','81ff')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','810c')
	uart.gphy_wr('f140','8129')
	uart.gphy_wr('f140','8173')
	uart.gphy_wr('f140','81e7')
	uart.gphy_wr('f140','81c5')
	uart.gphy_wr('f140','8108')
	uart.gphy_wr('f140','8106')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8101')
	uart.gphy_wr('f140','8108')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8106')
	uart.gphy_wr('f140','8104')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8101')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','810c')
	uart.gphy_wr('f140','8129')
	uart.gphy_wr('f140','8173')
	uart.gphy_wr('f140','81e7')
	uart.gphy_wr('f140','81c5')
	uart.gphy_wr('f140','81c0')
	uart.gphy_wr('f140','81a8')
	uart.gphy_wr('f140','8111')
	uart.gphy_wr('f140','810c')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','8100')
	uart.gphy_wr('f140','81c0')
	uart.gphy_wr('f140','81a8')
	uart.gphy_wr('f140','8111')
	uart.gphy_wr('f140','8103')

def packet_send_start(uart):
	packet_IPG(uart)
	packet_start(uart)
	packet_IPG(uart)
	
def packet_send_arp(uart):
	packet_IPG(uart)
	packet_start(uart)
	packet_IPG(uart)
	


	





	
