#This Script Reads the Data from INA219 Current Shunt Monitors for Power Measurements
#Also Modifies Analog and Digital 1.1V Voltage 
#Basic Commands used :-
#		read all 				----------> Reads all the 3 Voltage Sources and its corresponding current and Power Measurements
#		modify analog 'value'	----------> Modifies the Analog TPS Switching Regulator in order Modify analog 1.1v
#		modify analog 'value'	----------> Modifies the Digital TPS Switching Regulator in order Modify digital 1.1v

#Author - Hari Udayakumar   email - h.udayakumar.ee@lantiq.com

from etc_ftdi 				import *
from etc_ftdi.etc_header 	import *
from etc_ftdi.etc_i2c_cmds 	import *
from etc_uart 				import *
from ps_main 				import *
from results				import *
from results_xl				import *
import csv
import time
import shlex
import sys

def etc_pwr(d):
	#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
	Power_MM=[]
	for j in range(6):
		dataBV =[hex(I2C_ADDR[j]),] 
		for i in range(6):
			data = INA219_Reg_RRead(d,(I2C_ADDR[j]<<1),INA219_REG[i])
			if i == 1:
				dataBV += round((int(data.encode('hex'),16)*0.01),4),
			elif i == 2:
				dataBV += round((int(data.encode('hex'),16)>>3)*0.004,4),
			elif i == 3:
				dataBV += round((int(data.encode('hex'),16)*PWR_LSB[j]),4),
			elif i == 4:
				dataBV += round((int(data.encode('hex'),16)*CUR_LSB[j]),4),
			else:
				dataBV += data.encode('hex'),	
		Power_MM += dataBV,	
	return Power_MM
	
#Set this Variable to 
EXC_PD = False

#---------------------------------------------
#Reset the Device
#---------------------------------------------
#power_switch_off()
#time.sleep(30)
#power_switch_on()
#time.sleep(30)

#This Function enables MPSSE Mode and Initializes FTDI Device
file = sys.argv
d=MPSSE_I2C(0)
d.DevConf_I2C()

#This object access the UART 2 of ETC For PDI Register Read Write
uart_etc = uart_reg_rw(1,115200)

#Power Module Calibaration Configuration
#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])	
	
#CSV File Generation	
csv_result1 = open(file[2]+'.csv','wb')
writer1 = csv.writer(csv_result1)	

#Excel File Generation
w = creating_xl_file(file[2]+'_paul.xlsx')
w_s1 = creating_xl_sheet(w)
ws_header(w_s1,3)
	
#csv_result2 = open('ETC_Power_measurements_2.csv','wb')
#writer2 = csv.writer(csv_result2)
fw_version = uart_etc.gphy_mdio_rd(0,0x1E)
writer1.writerows([['Device Fuse Register Read','',],['FW Version',fw_version],['Sl.no','REG ADDR','REG VAL']])

#Log Device Information 
device_reg_baddr = 0xFA20
count = 0

print('stage1 complete')
for i in range(0xFA10,0xFA46):
	count = i-0xFA10+1
	device_reg_value = '0x'+uart_etc.gphy_rd(hex(i)[2:])
	writer1.writerows([[str(count),hex(i),device_reg_value],])
		
#Read GPHY0- Data - IP Version of GPHY0
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x70A)
count = count+1
writer1.writerows([[str(count),'1F.70A',mmd_reg_val],])

#GPHY0 - Transmitter Amplitude
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x709)
count = count+1
writer1.writerows([[str(count),'1F.70D',mmd_reg_val],])	

#GPHY0 - BDEV
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x70F)
count = count+1
writer1.writerows([[str(count),'1F.70F',mmd_reg_val],])

#GPHY0 - BDEV
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x710)
count = count+1
writer1.writerows([[str(count),'1F.710',mmd_reg_val],])	

for i in range(0xD80,0xD98):
	mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,i)
	count = count+1
	writer1.writerows([[str(count),'1F.'+hex(i)[2:],mmd_reg_val],])

#-----------------------------------------------
#Switch Programming - 0xE001 - 0x0003
#-----------------------------------------------	
uart_etc.gphy_wr('e001','0003')
s_reg_val = '0x0'+uart_etc.gphy_rd('e001')
writer1.writerows([[str(count),'E001',s_reg_val],])
#-----------------------------------------------
#EXC PD - Condition 
#-----------------------------------------------
if EXC_PD == True:
	for i in range(4):
		uart_etc.gphy_mmd_wr(i,0x1FF,0x0000)
else:
	for i in range(4):
		uart_etc.gphy_mmd_wr(i,0x1FF,0x0020)		
	
	
for i in range(4):
	mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(i,0x1FF)
	writer1.writerows([[str(count),'GPHY'+str(i)+'-->1F.1FF',mmd_reg_val],])

print('Register Dump Finished')	
#------------------------------------------------
#Reading the Input File
#------------------------------------------------
testcase_list = open(file[1],'r')
row_no = 1
while True:
	testcase = testcase_list.readline()
	if testcase == "DONE":
		break
	commands = shlex.split(testcase)
	#Measure Power at Power on Condition
	if commands[1] == '0':
		reg_addr = 'fa01'
		reg_data = '0x'+uart_etc.gphy_rd(reg_addr)
		description = commands[2]
		Pwr_MM_Restults_avg=[]
		for lp in range(3):
			Pwr_MM_Results = etc_pwr(d)
			Pwr_MM_Restults_avg += Pwr_MM_Results,
			time.sleep(5)
		results_generation(writer1,Pwr_MM_Results,reg_addr,reg_data,description)
		add_mm_ws(w_s1,row_no,description,Pwr_MM_Restults_avg,3)
		time.sleep(5)
	else:
		readback = []
		des_cnt = 0
		for no_wr in range(int(commands[1])):
			reg_addr = commands[2+(no_wr*2)]	
			reg_data = commands[3+(no_wr*2)]
			des_cnt	 = 4 + no_wr*2
			uart_etc.gphy_wr(reg_addr,reg_data)	
			#print(reg_addr +'---->'+ '0x'+uart_etc.gphy_rd(reg_addr))
		description = commands[des_cnt]
		for lp in range(3):
			Pwr_MM_Results = etc_pwr(d)
			Pwr_MM_Restults_avg += Pwr_MM_Results,
	results_generation(writer1,Pwr_MM_Results,reg_addr,'0x'+reg_data,description)
	add_mm_ws(w_s1,row_no,description,Pwr_MM_Restults_avg,3)
	time.sleep(5)
	row_no = row_no + 1
csv_result1.close()	
w.close()

