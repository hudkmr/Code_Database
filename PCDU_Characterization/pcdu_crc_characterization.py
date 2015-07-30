from etc_uart import *
from etc_i2c_tps import *
from misc import *
from gpib import *

from xlutils.copy import copy
from xlrd import *

import logging
import time

temp_enable = False

#ETC Register for PCDU Characterization
PCDU_5 = 'f101'
PCDU_6 = 'f10b'
BM_RAM_ADDR='e044'
BM_RAM_CTRL='e045'
BM_RAM_VAL0='e043'
BM_RAM_VAL1='e042'
RX_CRC_ERROR_CNT_REG='0021'
PCDU5_RX_MREQ='f169'
PCDU5_RX_KVAL='f168'
PCDU5_TX_MREQ='f161'
PCDU5_TX_KVAL='f160'
column_no=2
temp_list = ['25']

def enable_rmon_counters(uart):
	uart.gphy_wr('e080','0001')
	uart.gphy_wr('e082','0001')
	uart.gphy_wr('e084','0001')
	uart.gphy_wr('e086','0001')
	uart.gphy_wr('e088','0001')
	uart.gphy_wr('e08A','0001')
	
def clear_rmon_counters(uart):
	uart.gphy_wr('e081','0003')
	uart.gphy_wr('e083','0003')
	uart.gphy_wr('e085','0003')
	uart.gphy_wr('e087','0003')
	uart.gphy_wr('e089','0003')
	uart.gphy_wr('e08B','0003')

def rmon_counter_crc_read(uart,port):
	data=[]
	uart.gphy_wr(BM_RAM_ADDR,'0021')
	rmon_ctrl_val = int_to_str(0x8000 | port)
	uart.gphy_wr(BM_RAM_CTRL,rmon_ctrl_val)
	data = (int(uart.gphy_rd(BM_RAM_VAL1),16) << 16) | int(uart.gphy_rd(BM_RAM_VAL1),16)
	return hex(data)
	
def rmon_counter_read(uart,register,port):
	data=[]
	uart.gphy_wr(BM_RAM_ADDR,register)
	rmon_ctrl_val = int_to_str(0x8000 | port)
	uart.gphy_wr(BM_RAM_CTRL,rmon_ctrl_val)
	data = (int(uart.gphy_rd(BM_RAM_VAL1),16) << 16) | int(uart.gphy_rd(BM_RAM_VAL1),16)
	return hex(data)	
	
def pcdu_tx_dly_loop(uart_port):
	#Varying PCDU_5 TX Delay Routine
	for i in range(9):
		logging.info("PCDU_5 Register Value = %s",uart_port.gphy_rd(PCDU_5))
		#logging.info("PCDU_6 Register Value = %s",uart_port.gphy_rd(PCDU_6))
		
		#Program PCDU for New Values
		pcdu_val = int_to_str(0x0200| i)
		uart_port.gphy_wr(PCDU_5,pcdu_val)
		#uart_port.gphy_wr(PCDU_6,pcdu_val)
		
		#Delay
		time.sleep(60)
		
		#Read the RX CRC Values
		logging.info("RX CRC Error on Port 5 = %s",rx_crc_error_counter(uart_port))
		logging.info("RX Total Packets on Port 5 = %s",rx_total_packets_counter(uart_port))
		
		logging.info("\n")	
		
def pcdu_txdly_rxdly_loop(uart,result,voltage):
	offset = 2
	clear_rmon_counters(uart)
	packet_send_start(uart)
	for txd in range(8):
		for rxd in range(8):
			
			#Program the PCDU Delay Value
			pcdu_val = int_to_str(rxd << 7 | txd )
			uart.gphy_wr(PCDU_5,pcdu_val)
			print ('PCDU_5 Reg Value - '+uart.gphy_rd(PCDU_5))
			
			#TSample Read with 10 Sec Delay
			time.sleep(10)
			
			#Read RMON Counters
			rx_crc_cnt = rmon_counter_crc_read(uart,5)
			rx_total_frame_cnt = rmon_counter_read(uart,'001F',5)
			tx_total_frame_cnt = rmon_counter_read(uart,'000C',5)
			pcdu_reg_val =uart.gphy_rd(PCDU_5)
			tx_k_val = uart.gphy_rd(PCDU5_TX_KVAL)
			tx_m_val = uart.gphy_rd(PCDU5_TX_MREQ)
			rx_k_val = uart.gphy_rd(PCDU5_RX_KVAL)
			rx_m_val = uart.gphy_rd(PCDU5_RX_MREQ)
			
			#Log the data in txt and excel format
			logging.info("RX CRC Error on Port 5 = %s",rx_crc_cnt)
			logging.info("RX Total Packets on Port 5 = %s",rx_total_frame_cnt)
			logging.info("TX Total Packets on Port 5 = %s",tx_total_frame_cnt)
			logging.info("PCDU_5 Register Value = %s",pcdu_reg_val)
			logging.info("\n")	
		
			#Excel Result Logging
			sl_no = txd*8 +rxd
			result.get_sheet(0).write(offset+sl_no,0,(sl_no+1))				#Column 1 - is Serial No
			result.get_sheet(0).write(offset+sl_no,1,voltage)
			result.get_sheet(0).write(offset+sl_no,2,int(tx_total_frame_cnt,16))
			result.get_sheet(0).write(offset+sl_no,3,int(rx_total_frame_cnt,16))
			result.get_sheet(0).write(offset+sl_no,4,int(rx_crc_cnt,16))
			result.get_sheet(0).write(offset+sl_no,5,pcdu_reg_val)
			result.get_sheet(0).write(offset+sl_no,6,tx_k_val)
			result.get_sheet(0).write(offset+sl_no,7,tx_m_val)
			result.get_sheet(0).write(offset+sl_no,8,tx_k_val)
			result.get_sheet(0).write(offset+sl_no,9,tx_m_val)
					
	
def pcdu_m_value_loop(uart,result,voltage,column_no,temperature):
	i=0
	offset = 2
	clear_rmon_counters(uart)
	packet_send_start(uart)
	while(i <= 0x90):
		#Program PCDU for New Values
		pcdu_val = int_to_str(i)
		uart.gphy_wr(PCDU5_TX_MREQ,pcdu_val)
		print ('PCDU5_TX_MREQ Reg Value - '+uart.gphy_rd(PCDU5_TX_MREQ))
		time.sleep(10)
		
		#Read RMON Counters
		rx_crc_cnt = rmon_counter_crc_read(uart,5)
		rx_total_frame_cnt = rmon_counter_read(uart,'001F',5)
		tx_total_frame_cnt = rmon_counter_read(uart,'000C',5)
		pcdu_reg_val =uart.gphy_rd(PCDU_5)
		tx_k_val = uart.gphy_rd(PCDU5_TX_KVAL)
		tx_m_val = uart.gphy_rd(PCDU5_TX_MREQ)
		rx_k_val = uart.gphy_rd(PCDU5_RX_KVAL)
		rx_m_val = uart.gphy_rd(PCDU5_RX_MREQ)
		
		#Log the data in txt and excel format
		logging.info("RX CRC Error on Port 5 = %s",rx_crc_cnt)
		logging.info("RX Total Packets on Port 5 = %s",rx_total_frame_cnt)
		logging.info("TX Total Packets on Port 5 = %s",tx_total_frame_cnt)
		logging.info("PCDU_5 Register Value = %s",pcdu_reg_val)
		logging.info("\n")	
	
		#Excel Result Logging
		sl_no = (i/4)
		result.get_sheet(column_no).write(sl_no+offset,0,sl_no+1)
		result.get_sheet(column_no).write(sl_no+offset,1,temperature)
		result.get_sheet(column_no).write(sl_no+offset,2,voltage)
		result.get_sheet(column_no).write(sl_no+offset,3,int(tx_total_frame_cnt,16))
		result.get_sheet(column_no).write(sl_no+offset,4,int(rx_total_frame_cnt,16))
		result.get_sheet(column_no).write(sl_no+offset,5,int(rx_crc_cnt,16))
		result.get_sheet(column_no).write(sl_no+offset,6,pcdu_reg_val)
		result.get_sheet(column_no).write(sl_no+offset,7,tx_k_val)
		result.get_sheet(column_no).write(sl_no+offset,8,tx_m_val)
		result.get_sheet(column_no).write(sl_no+offset,9,tx_k_val)
		result.get_sheet(column_no).write(sl_no+offset,10,tx_m_val)	
		crc_comp = '=F'+str(sl_no+offset+1)+'-'+'F'+str(sl_no+offset)
		result.get_sheet(column_no).write(sl_no+offset,11,crc_comp)	
		#Delay
		time.sleep(2)
		i=i+4



def etc_silicon_type(uart):
	type = uart.gphy_rd('FA44')
	if type == '0001':
		return 'TT'
	elif type == '0005':
		return 'FFF'
	elif type == '0006':
		return 'FF'
	elif type == '0007':
		return 'SSS'
	elif type == '0008':
		return 'SS'
	elif type == '0009':
		return 'FS'
	elif type == '000A':
		return 'SF'	
	elif type == '000B':
		return 'FFrc'
	elif type == '000C':
		return 'SSrc'
	else:
		return 'Unknow_'+type
		
	
#Main Routine
def main():
	now = time.strftime("%d%H%M")
	uart_port = uart_reg_rw(0,115200)
	if temp_enable == True:
		temp_c = gpib_init()
	else:
		temperature = '25C'
	for t in temp_list:
		if temp_enable == True:
			espec_setT(temp_c,t)
			time.sleep(300)
			temperature = espec_readT(temp_c)
		silicon_type = etc_silicon_type(uart_port)
		logging.basicConfig(filename=('PCDU_Characterization_'+silicon_type+'_'+temperature+'_'+now+'.txt'), level=logging.INFO)
		logging.info("Started at %s"%current_time())
		uart_port.gphy_close()
		#Result Excel Sheet
		result = copy(open_workbook('pcdu_template.xls'))
		for i in range(20):
			voltage = str(modify_1v1(i+160))
			uart_port = uart_reg_rw(0,115200)
			
			#-----------------------------------------
			#pcdu routine
			#-----------------------------------------
			#Step 1 - Enable RMON Counters
			enable_rmon_counters(uart_port)
			
			#Step 2 - Insert Packet
			packet_ext_enable(uart_port)
				
			#10Sec Delay 
			print('Reset Request Register value - ' + uart_port.gphy_rd('FA01'))
			uart_port.gphy_wr(PCDU_5,'0400')
			uart_port.gphy_wr(PCDU5_TX_KVAL,'0040')
			
			#Call PCDU Delay Routine
			pcdu_m_value_loop(uart_port,result,voltage,i,temperature)
			#pcdu_txdly_rxdly_loop(uart_port,result)
			uart_port.gphy_close()
		result.save('PCDU_Characterization_'+silicon_type+'_'+temperature+'_'+now+'.xls')
		logging.info("Ended at %s"%current_time())
	
if __name__ == '__main__':
	main()
	
#End of the Routine