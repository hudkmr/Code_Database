#------------------------------------------------------------------------------
#Author - Hari Udayakumar h.udayakumar.ee@lantiq.com
#
#Refer INA219 Spec for Detailed Calculation on Current LSB Value
#Note the Current LSB Value choosen is 200e-6
#
#--------------------------------------------------------------------------------

from etc_ftdi import *
from etc_ftdi.etc_header import *
from etc_ftdi.etc_i2c_ina219 import *


class etc_main():
	
	def __init__(self):
		self.d = MPSSE_I2C(0)
		
	def etc_i2c_init(self):	
		#This Function enables MPSSE Mode and Initializes FTDI Device
		self.d.DevConf_I2C()
	
	def etc_conf_cal(self):	
		#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V 
		Flash_data=[[],[]]
		Flash_addr=['00','01','02','03','04','05','06','07','08','09','0a','0b']
		for dev in range(2):
			for ix in range(12):
				data = INA219_Reg_RRead(self.d,(FLD_ADDR[dev]<<1),Flash_addr[ix],RW)
				Flash_data[dev].append(hex(int(data.encode('hex'),16))[2:])
				print hex(2*ix)[2:],Flash_data[dev][ix]
				
		for dev in range(2):
			conf_val = Flash_data[dev][6]
			if (int(conf_val,16) == 0) or (int(conf_val,16) == 0xffff):
				print "Callibration info not found"
			cal_val = [Flash_data[dev][0],Flash_data[dev][2],Flash_data[dev][4]]	
			for i in range(3):
				data=INA219_Reg_Write(self.d,(I2C_ADDR[i + (3*dev)]<<1),INA219_REG[0],conf_val,RW)
				data=INA219_Reg_Write(self.d,(I2C_ADDR[i + (3*dev)]<<1),INA219_REG[5],cal_val[i],RW)
				
	def etc_config_cal(self):		
			for i in range(9):
				data=INA219_Reg_Write(self.d,(I2C_ADDR[i]<<1),INA219_REG[0],'019F',RW)
				data=INA219_Reg_Write(self.d,(I2C_ADDR[i]<<1),INA219_REG[5],'8000',RW)			
	
	def etc_pwr(self):
		#Reading Bus Voltage across All INA219 - #Note 0.004 - 1 LSB 
		Power_MM=[]
		for j in range(9):
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
		for j in range(9):
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
		print("Power Module 1:")
		for i in range(9):
				print("\t%s\t%.2f\t%.2f\t%.2f\t\t%.2f"%(hex(I2C_ADDR[i]),Power_MM[i][2],Power_MM[i][1],Power_MM[i][4],Power_MM[i][3]))
				if i==2:
					print("\n\nPower Module 2:")
				if i==5:
					print("\n\nPower Module 3:")		
		
		
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
		
			
		