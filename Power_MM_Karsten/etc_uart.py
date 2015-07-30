from etc_ftdi import UART
from etc_ftdi.etc_header 	import *

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
		
	def gphy_mdio_rd(self,port,reg):
		addr = self._int_to_str(0x2 << 10 | port << 5 | reg)
		wr_command = 'w  f408 '+addr
		self.d.WR(wr_command)
		rd_command = 'r f409'
		output = self.d.RD(rd_command)
		return output
	
	def gphy_mdio_wr(self,port,reg,data):
		addr = self._int_to_str(0x1 << 10 | port << 5 | reg)
		wr_command = 'w  f408 '+addr
		self.d.WR(wr_command)
		wr_data = 'w f40a '+hex(data)[2:]
		self.d.WR(wr_data)
		
	def gphy_mmd_rd(self,port,reg):
		mmdr_ctrl_w = self._int_to_str(1 << 10 | port << 5 | 0xD)
		mmdr_ctrl_r = self._int_to_str(2 << 10 | port << 5 | 0xD)
		mmdr_data_r = self._int_to_str(2 << 10 | port << 5 | 0xE)
		mmdr_data_w = self._int_to_str(1 << 10 | port << 5 | 0xE)
		wr_command = 'w f40b 0000'		#Disable Autopolling
		self.d.WR(wr_command)
		wr_command = 'w f40A 001F'
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_ctrl_w
		self.d.WR(wr_command)
		wr_command = 'w f40A '+self._int_to_str(reg)
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_data_w
		self.d.WR(wr_command)
		wr_command = 'w f40A 401F'
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_ctrl_w
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_data_r
		self.d.WR(wr_command)
		rd_command = 'r f409'
		output = self.d.RD(rd_command)
		wr_command = 'w f40b 006F'		#Enable Autopolling
		self.d.WR(wr_command)
		return output
	
	def gphy_mmd_wr(self,port,reg,data):
		mmdr_ctrl_w = self._int_to_str(1 << 10 | port << 5 | 0xD)
		mmdr_ctrl_r = self._int_to_str(2 << 10 | port << 5 | 0xD)
		mmdr_data_r = self._int_to_str(2 << 10 | port << 5 | 0xE)
		mmdr_data_w = self._int_to_str(1 << 10 | port << 5 | 0xE)
		
		wr_command = 'w f40b 0000'		#Disable Autopolling
		self.d.WR(wr_command)
		wr_command = 'w f40A 001F'
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_ctrl_w
		self.d.WR(wr_command)
		wr_command = 'w f40A '+self._int_to_str(reg)
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_data_w
		self.d.WR(wr_command)
		wr_command = 'w f40A 401F'
		self.d.WR(wr_command)
		wr_command = 'w f408 '+mmdr_ctrl_w
		self.d.WR(wr_command)
		wr_data = 'w f40A '+self._int_to_str(data)
		self.d.WR(wr_data)
		wr_command = 'w f408 '+mmdr_data_w
		self.d.WR(wr_command)
		wr_command = 'w f40b 006F'		#Enable Autopolling
		self.d.WR(wr_command)

	
	def _int_to_str(self,val):
		temp = hex(val)[2:]
		while len(temp) < 4:
			temp = '0'+temp
		return temp	
		
	def gphy_close(self):
		self.d.Close()

