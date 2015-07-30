from etc_ftdi import *
from etc_ftdi.etc_header import *
from etc_ftdi.etc_i2c_ina219 import *


class etc_main():
	
	def __init__(self):
		self.d = MPSSE_I2C(0)
		
	def etc_i2c_init(self):	
		#This Function enables MPSSE Mode and Initializes FTDI Device
		self.d.DevConf_I2C()
		#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
		for i in range(6):
			data=INA219_Reg_Write(self.d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF',RW)
			data=INA219_Reg_Write(self.d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i],RW)
	
	def etc_pwr(self):
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		Power_MM=[]
		for j in range(6):
			dataBV =[hex(I2C_ADDR[j]),] 
			for i in range(6):
				data = INA219_Reg_RRead(self.d,(I2C_ADDR[j]<<1),INA219_REG[i],RW)
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
				
	def etc_ana_mod(self,val):
		#Program TPS Device with the Required Value	
		data=INA219_Reg_Write(self.d,(TPS_ADDR[0]<<1),"01",val,RW)	
		time.sleep(2)
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		data = INA219_Reg_RRead(self.d,(I2C_ADDR[0]<<1),INA219_REG[2],RW)
		data.encode('hex')
		dataBV = round((int(data.encode('hex'),16)>>3)*0.004,4)
		time.sleep(2)
		return dataBV
		
	def etc_dig_mod(self,val):
		#Program TPS Device with the Required Value	
		data=INA219_Reg_Write(self.d,(TPS_ADDR[1]<<1),"01",val,RW)	
        
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		data = INA219_Reg_RRead(self.d,(I2C_ADDR[3]<<1),INA219_REG[2],RW)
		data.encode('hex')
		dataBV = round((int(data.encode('hex'),16)>>3)*0.004,4)
		time.sleep(2)
		return dataBV
		
	def etc_rd_all(self):
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		Power_MM=[]
		for j in range(6):
			dataBV=[]
			for i in range(6):
				data = INA219_Reg_RRead(self.d,(I2C_ADDR[j]<<1),INA219_REG[i],RW)
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
		
		
	def etc_ana_mod_rd(self,val):
		TPS_WR_Value = hex(val)	
		TPS_WR_Value = TPS_WR_Value[2:] + "00"
		#Program TPS Device with the Required Value	
		data=INA219_Reg_Write(self.d,(TPS_ADDR[0]<<1),"01",TPS_WR_Value,RW)	
		time.sleep(2)
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		data = INA219_Reg_RRead(self.d,(I2C_ADDR[0]<<1),INA219_REG[2],RW)
		data.encode('hex')
		dataBV = round((int(data.encode('hex'),16)>>3)*0.004,6)
		time.sleep(2)
		#Printing all the Results Read
		print("\t\tAddr\tBV(V)")
		print("Analog:")
		print("\t\t%s\t%.2f"%(hex(I2C_ADDR[0]),dataBV))
		
		
	def etc_dig_mod_rd(self,val):
		TPS_WR_Value = hex(val)	
		TPS_WR_Value = TPS_WR_Value[2:] + "00"
		#Program TPS Device with the Required Value	
		data=INA219_Reg_Write(self.d,(TPS_ADDR[1]<<1),"01",TPS_WR_Value,RW)	
        
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		data = INA219_Reg_RRead(self.d,(I2C_ADDR[3]<<1),INA219_REG[2],RW)
		data.encode('hex')
		dataBV = round((int(data.encode('hex'),16)>>3)*0.004,6)

		#Printing all the Results Read
		print("\t\tAddr\tBV(V)")
		print("Digital:")
		print("\t\t%s\t%.2f"%(hex(I2C_ADDR[3]),dataBV))
		
	def Close(self):
		self.d.close()
		
			
		