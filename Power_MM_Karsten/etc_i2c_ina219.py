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
from results				import *
import csv
import time

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
EXC_PD = True

#This Function enables MPSSE Mode and Initializes FTDI Device
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
csv_result1 = open('ETC_Power_measurements.csv','wb')
writer1 = csv.writer(csv_result1)	
	
#csv_result2 = open('ETC_Power_measurements_2.csv','wb')
#writer2 = csv.writer(csv_result2)

writer1.writerows([['Device Fuse Register Read','',],['Sl.no','REG ADDR','REG VAL']])
#Log Device Information 
device_reg_baddr = 0xFA20
count = 0
for i in range(0xFA10,0xFA46):
	count = i-0xFA10+1
	device_reg_value = '0x'+uart_etc.gphy_rd(hex(i)[2:])
	writer1.writerows([[str(count),hex(i),device_reg_value],])
		
#Read GPHY0- Data - IP Version of GPHY0
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x70A)
writer1.writerows([[str(count+1),'1F.70A',mmd_reg_val],])

#GPHY0 - Transmitter Amplitude
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x70D)
writer1.writerows([[str(count+1),'1F.70D',mmd_reg_val],])	

#GPHY0 - BDEV
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x70F)
writer1.writerows([[str(count+1),'1F.70F',mmd_reg_val],])

#GPHY0 - BDEV
mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,0x710)
writer1.writerows([[str(count+1),'1F.710',mmd_reg_val],])	

for i in range(0xD80,0xD98):
	mmd_reg_val = '0x0'+uart_etc.gphy_mmd_rd(0,i)
	writer1.writerows([[str(count+1),'1F.'+hex(i)[2:],mmd_reg_val],])


if EXC_PD == True:
	for i in range(4):
		uart_etc.gphy_mmd_wr(i,0x1FF,0x20)
else:
	for i in range(4):
		uart_etc.gphy_mmd_wr(i,0x1FF,0x00)		
			
#Measure Power at Power on Condition
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement at Power on Condition')
time.sleep(5)

#Measure Power - All Port Enabled
uart_etc.gphy_wr('fa01','0000')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - All Port Enabled')	
time.sleep(5)

#Measure Power - Uc Disabled
uart_etc.gphy_wr('fa01','0010')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - Uc Disabled')	
time.sleep(5)

#Measure Power - SGMII PHY in Low Power Mode
uart_etc.gphy_wr('d009','000c')	
reg_value = '0x'+uart_etc.gphy_rd('d009')
reg_addr = 'd009'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - SGMII PHY in Low Power Mode')
time.sleep(5)

#Measure Power - SGMII Port Disabled
uart_etc.gphy_wr('fa01','0030')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - SGMII Port Disabled')
time.sleep(5)

#Measure Power - GPHY0 Disabled
uart_etc.gphy_wr('fa01','0031')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - GPHY0 Disabled')
time.sleep(5)
	

#Measure Power - GPHY0,GPHY1 Disabled
uart_etc.gphy_wr('fa01','0033')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - GPHY0,GPHY1 Disabled')
time.sleep(5)

#Measure Power - GPHY0,GPHY1,GPHY2 Disabled
uart_etc.gphy_wr('fa01','0037')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - GPHY0,GPHY1,GPHY2 Disabled')
time.sleep(5)

#Measure Power - GPHY0,GPHY1,GPHY2,GPHY3 Disabled
uart_etc.gphy_wr('fa01','003F')	
reg_value = '0x'+uart_etc.gphy_rd('fa01')
reg_addr = 'fa01'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - GPHY0,GPHY1,GPHY2,GPHY3 Disabled')
time.sleep(5)

#Measure Power - ROPLL Disable
uart_etc.gphy_wr('f980','0000')	
uart_etc.gphy_md('f98c','0040','0040')	
reg_value = '0x'+uart_etc.gphy_rd('f980')
reg_addr = 'f980'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement - ROPLL Disable')			
time.sleep(5)

#Measure Power with CDB Disable
uart_etc.gphy_md('f88c','0040','0040')
uart_etc.gphy_wr('f880','0000')	
reg_value = '0x0000'
reg_addr = 'f880'
Pwr_MM_Results = etc_pwr(d)
results_generation(writer1,Pwr_MM_Results,reg_value,reg_addr,'Power Measurement with CDB Disable')	
time.sleep(5)

csv_result1.close()	

