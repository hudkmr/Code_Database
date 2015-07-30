from etc_uart import *
import os,sys
import csv
import shutil
import sys

commands = sys.argv

#Log CSV File for ETC Register Values
csv_file_name = 'ETC_Register_Log_'+commands[1]+'.csv'
csv_result = open(csv_file_name,'wb')
writer = csv.writer(csv_result)

#Updating CSV result with Link Speed
writer.writerows([['ETC Registers',],''])
writer.writerows([['Sl.no','Register Address','Value'],])

#Open UART 1 
uart = uart_reg_rw(1,115200)

for i in range(int(commands[2],16),int(commands[3],16)):
	sl_no = str(i-+1)
	addr  = hex(i)[2:]
	data  = '0x'+uart.gphy_rd(hex(i)[2:])
	print data
	writer.writerows([[sl_no,addr,data],])
	
csv_result.close()	


