#This Script Reads the Data from INA219 Current Shunt Monitors for Power Measurements
#Also Modifies Analog and Digital 1.1V Voltage 
#Basic Commands used :-
#		read all 				----------> Reads all the 3 Voltage Sources and its corresponding current and Power Measurements
#		modify analog 'value'	----------> Modifies the Analog TPS Switching Regulator in order Modify analog 1.1v
#		modify analog 'value'	----------> Modifies the Digital TPS Switching Regulator in order Modify digital 1.1v

#Author - Hari Udayakumar   email - h.udayakumar.ee@lantiq.com

from etc_ftdi 				import MPSSE_I2C
from etc_ftdi.etc_header 	import *
from etc_ftdi.etc_i2c_cmds 	import *
from etc_uart 				import *
import shlex
import sys

def Power_MM():
	#Reading Shunt Voltage across All INA219
	Pwr=[]
	dataSV=[]
	for i in range(6):
		data =INA219_Reg_RRead(d,(I2C_ADDR[i]<<1),INA219_REG[1])
		dataSV += round(int(data.encode('hex'),16)*0.01,2),
		#print("Shunt Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[i],Voltage))	
	Pwr.append(dataSV)
	#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
	dataBV=[]
	for i in range(6):
		data =INA219_Reg_RRead(d,(I2C_ADDR[i]<<1),INA219_REG[2])
		dataBV += round(float(int(data.encode('hex'),16)>>3)*0.004,2),
	Pwr.append(dataBV)
	
	#Reading Power Value across All INA219
	dataPW=[]
	for i in range(6):
		data=INA219_Reg_RRead(d,(I2C_ADDR[i]<<1),INA219_REG[3])
		dataPW += round(float(int(data.encode('hex'),16))*(PWR_LSB[i]),2),
	Pwr.append(dataPW)	
		
	dataCA=[]	
	#Reading Current across All INA219
	for i in range(6):
		data=INA219_Reg_RRead(d,(I2C_ADDR[i]<<1),INA219_REG[4])
		dataCA += round(float(int(data.encode('hex'),16))*CUR_LSB[i],2),
	Pwr.append(dataCA)	
	return 	Pwr
		
#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()

#This object access the UART 2 of ETC For PDI Register Read Write
uart_etc = uart_reg_rw(1,115200)
input_file = sys.argv
#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])
input = raw_input('>')	
commands = shlex.split(input)
error = NONE
while True:	
			if commands[0] == 'quit':
				break
			elif commands[0] == 'read':
				if commands[1] == 'all':
					Pwr_MM_Results = Power_MM()
					#Printing all the Results Read
					print("\tAddr\tBV(V)\tSV(mV)\tCurrent(mA)\tPower(mW)")
					print("Analog:")
					for i in range(6):
						print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),Pwr_MM_Results[1][i],Pwr_MM_Results[0][i],Pwr_MM_Results[3][i],Pwr_MM_Results[2][i]))
						if i==2:
							print("\n\nDigital:")
				else:
					error = -1				
			elif commands[0] == 'modify':
				if commands[1] == 'analog':
					#Program TPS Device with the Required Value	
					TPS_WR_Value = hex(int(commands[2]))[2:]+'00'
					data=INA219_Reg_Write(d,(TPS_ADDR[0]<<1),TPS_REG[0],TPS_WR_Value)	
					#Reading Back the the Analog Voltage
					Pwr_MM_Results = Power_MM()
					print("\t\tAddr\tBV(V)")
					print("Analog:")
					print("\t\t%s\t%.2f"%(hex(I2C_ADDR[0]),Pwr_MM_Results[1][0]))
				elif commands[1] == 'digital':	
					#Program TPS Device with the Required Value	
					TPS_WR_Value = hex(int(commands[2]))[2:]+'00'
					data=INA219_Reg_Write(d,(TPS_ADDR[1]<<1),TPS_REG[0],TPS_WR_Value)	
					#Reading Back the the Digital Voltage
					Pwr_MM_Results = Power_MM()
					print("\t\tAddr\tBV(V)")
					print("Digital:")
					print("\t\t%s\t%.2f"%(hex(I2C_ADDR[3]),Pwr_MM_Results[1][3]))
				else:
					error = -1	
			elif commands[0] == 'r':
				print uart_etc.gphy_rd(commands[1])
			elif commands[0] == 'w':
				uart_etc.gphy_wr(commands[1],commands[2])
			elif commands[0] == 'm':
				uart_etc.gphy_wr(commands[1],commands[2],commands[2])	
			else:
					error = -1					
			if error is not 0:
				print('Command not Recognised')
			input = raw_input('>')	
			commands = shlex.split(input)	
					
					
					
	
			
	

	

			
			


	

