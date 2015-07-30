#This Function calls the stc_data_transfer_process
import subprocess
import time
from results import *

def etc_link_register(uart,value):
	uart.gphy_wr('f408',value)	
	output = uart.gphy_rd('f409')
	return output
			
def etc_link_speed(uart):
	link_speed_value = []
	for i in range(6):
		if i == 0:
			link_speed_value += etc_link_register(uart,'0818'),
		elif i == 1:
			link_speed_value += etc_link_register(uart,'0838'),
		elif i == 2:
			link_speed_value += etc_link_register(uart,'0858'),
		elif i == 3:
			link_speed_value += etc_link_register(uart,'0878'),
		elif i == 4:
			link_speed_value += etc_link_register(uart,'0898'),
	return link_speed_value

def etc_firmware_check(uart):
	firmware_version=[]
	for i in range(6):
		if i == 0:
			firmware_version += etc_link_register(uart,'081E'),
		elif i == 1:
			firmware_version += etc_link_register(uart,'083E'),
		elif i == 2:
			firmware_version += etc_link_register(uart,'085E'),
		elif i == 3:
			firmware_version += etc_link_register(uart,'087E'),
		elif i == 4:
			firmware_version += etc_link_register(uart,'089E'),
	return firmware_version		
		
def data_transfer(row_no,tr_size,rad,test_condition,result_folder,result_file):
	link=[]
	#link += etc_firmware_check(uart),
	if rad == True:
		command = 'stc_'+tr_size+'mb_rad'
		tcl_cmd = 'tclsh '+command+'.tcl'
		stc_data_transfer = subprocess.Popen(tcl_cmd)
	else:	
		command = 'stc_'+tr_size+'mb'
		tcl_cmd = 'tclsh '+command+'.tcl'
		stc_data_transfer = subprocess.Popen(tcl_cmd)
	if tr_size == '1000':	
		time.sleep(10)
	else:
		time.sleep(60)
	#link += etc_link_speed(uart),
	stc_data_transfer.wait()
	time.sleep(10)
	results_modification(row_no,command,test_condition,result_folder,result_file)
	shutil.rmtree(command)
	