from etc_i2c_ina219 import *

def etc_main():
	#This Function enables MPSSE Mode and Initializes FTDI Device
	d=MPSSE_I2C(0)
	d.DevConf_I2C()

	#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
	for i in range(6):
		data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
		data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])
		

	#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
	Power_MM=[]
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
		Power_MM += dataBV,	
	#Printing all the Results Read
	print("\tAddr\tBV(V)\tSV(mV)\tCurrent(mA)\tPower(mW)")
	print("Analog:")
	for i in range(6):
			print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),Power_MM[i][2],Power_MM[i][1],Power_MM[i][4],Power_MM[i][3]))
			if i==2:
				print("\n\nDigital:")	
				
			