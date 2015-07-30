from etc_uart import *
import os,sys
import csv
import shutil
from xlrd import *
from xlutils.copy import copy

def sgmii_phy_reg_rd(uart,phy_addr):
	uart.gphy_wr('d101',hex(i)[2:])
	uart.gphy_wr('d102','1010')
	phy_data = uart.gphy_rd('d100')
	return phy_data

#Log CSV File for ETC Register Values
device_no=raw_input('Enter device no:')
csv_file_name = 'ETC_Register_Log_'+device_no+'.csv'
csv_result = open(csv_file_name,'wb')
writer = csv.writer(csv_result)

#Updating CSV result with Link Speed
writer.writerows([['ETC Registers',],''])
writer.writerows([['Sl.no','Register Address','Value'],])

#Open UART 1 
uart = uart_reg_rw(1,115200)

for i in range(0x1000,0x1030):
	sl_no = str(i-0x1000+1)
	addr  = hex(i)[2:]
	#data  = uart.gphy_rd(hex(i)[2:])
	data = '0x'+sgmii_phy_reg_rd(uart,i)
	print data
	writer.writerows([[sl_no,addr,data],])
	
for i in range(0x1100,0x1130):
	sl_no = str(i-0x1100+1+0x30)
	addr  = hex(i)[2:]
	#data  = uart.gphy_rd(hex(i)[2:])
	data = '0x'+sgmii_phy_reg_rd(uart,i)
	print data
	writer.writerows([[sl_no,addr,data],])
	
for i in range(0x1200,0x1230):
	sl_no = str(i-0x1200+1+0x60)
	addr  = hex(i)[2:]
	#data  = uart.gphy_rd(hex(i)[2:])
	data = '0x'+sgmii_phy_reg_rd(uart,i)
	print data
	writer.writerows([[sl_no,addr,data],])

for i in range(0x1200,0x1230):
	sl_no = str(i-0x1200+1+0x90)
	addr  = hex(i)[2:]
	#data  = uart.gphy_rd(hex(i)[2:])
	data = '0x'+sgmii_phy_reg_rd(uart,i)
	print data
	writer.writerows([[sl_no,addr,data],])
	
for i in range(0x9000,0x9030):
	sl_no = str(i-0x9000+1+0xC0)
	addr  = hex(i)[2:]
	#data  = uart.gphy_rd(hex(i)[2:])
	data = '0x'+sgmii_phy_reg_rd(uart,i)
	print data
	writer.writerows([[sl_no,addr,data],])	
	
csv_result.close()	

