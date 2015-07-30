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
import shlex
from datetime import *

def Power_MM(d):
	#Reading Shunt Voltage across All INA219
	Pwr=[]
	for j in range(6):
		dataBV=[]
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
		Pwr += dataBV,	
	return Pwr
		
#This Function enables MPSSE Mode and Initializes FTDI Device
d=MPSSE_I2C(0)
d.DevConf_I2C()

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
			Pwr_MM_Results = Power_MM(d)
			#Printing all the Results Read
			print("\tAddr\tBV(V)\tSV(mV)\tCurrent(mA)\tPower(mW)")
			print("Analog:")
			for i in range(6):
				print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),Pwr_MM_Results[i][2],Pwr_MM_Results[i][1],Pwr_MM_Results[i][4],Pwr_MM_Results[i][3]))
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
			Pwr_MM_Results = Power_MM(d)
			print("\t\tAddr\tBV(V)")
			print("Analog:")
			print("\t\t%s\t%.2f"%(hex(I2C_ADDR[0]),Pwr_MM_Results[0][2]))
		elif commands[1] == 'digital':	
			#Program TPS Device with the Required Value	
			TPS_WR_Value = hex(int(commands[2]))[2:]+'00'
			data=INA219_Reg_Write(d,(TPS_ADDR[1]<<1),TPS_REG[0],TPS_WR_Value)	
			#Reading Back the the Digital Voltage
			Pwr_MM_Results = Power_MM(d)
			print("\t\tAddr\tBV(V)")
			print("Digital:")
			print("\t\t%s\t%.2f"%(hex(I2C_ADDR[3]),Pwr_MM_Results[3][2]))
		else:
			error = -1	

	else:
			error = -1					
	if error is not 0:
		print('Command not Recognised')
	input = raw_input('>')	
	commands = shlex.split(input)	

					
					
					
	
			
	

	

			
			


	

