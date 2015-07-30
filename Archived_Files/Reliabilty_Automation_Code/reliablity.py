#This Script Automates 
#Voltage Modification - 1.1V,1.045, 1.055
#Temperature Modification - 0C, 25C, 75C
#List of Python Library Required
from reliablity_header 	import *

#ES-240S3 Library for Temperature Control
from gpib import *

#FTDI Libraries for Modifying 1.1 Analog Voltage
from etc_abb_i2c_lib import *
from etc_i2c_tps import *

from ip9258 import *

from result import *
  
call_ippower('python fence_ip9258.py -a {0} -l {1} -p {2} -n 5 -o on'.format(IP, login, passwd))  
time.sleep(5)

gphy_com = UART(1)
gphy_com.Config(921600)

#Read the Reset Register FA01
output = gphy_com.RD('r fa01')
if output is not '0000':
	gphy_com.WR('w fa01 0000')
	output = gphy_com.RD('r fa01')
	print('GPHY addr FA01 - %s'%output)
	
#Time Stamp
date=date.today()
date_str =date.strftime("%d-%m-%y")

#Filelog for Debbuging Information
logging.basicConfig(filename='TT_Reliability_Testing_'+date_str+'.log',level=logging.DEBUG)
Time_Start = (time.strftime("%H:%M:%S")) + (time.strftime("%d/%m/%Y"))
print Time_Start
logging.debug(Time_Start)
#Voltage TPS Calculation 
TPS_Values=[]
for i in TPS_Voltage:
	TPS_Values += hex(int((i+0.60)/0.01))[2:] +'00',

#ESP-240S3 Temp Values Conversion	
ESP_Values=[]
for i in Temp_C:
	ESP_Values += 'S'+str(i),

#This Function enables Synchronous Bit Bang Mode and Initializes FTDI Device
d=BB_I2C(0)
d.DevConf(BAUD,DO_MASK_VAL,SYNC_MODE)	
print('I2C Device Configured for Synchronous Bit Bang Mode')
logging.debug('I2C Device Configured for Synchronous Bit Bang Mode')

#Configure ALL the I2C Device to a Full Scale Voltage Range of 16V
for i in range(6):
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[0],'01DF')
	data=INA219_Reg_Write(d,(I2C_ADDR[i]<<1),INA219_REG[5],CAL_VAL[i])
print('All the CSM Devices Configured')		
logging.debug('All the CSM Devices Configured')	
	
#Initialzing the Chamber
temp_chamber = gpib_init()
espec_chamberon(temp_chamber)	
logging.debug('Temperature Chamber Configured and Turned On')

#The First Loop is around Analog Voltage 1.1v		
for v in range(len(TPS_Values)):
		data = INA219_Reg_Write(d,(TPS_ADDR[0]<<1),TPS_REG[0],TPS_Values[v])
		time.sleep(2)
		data =INA219_Reg_RRead(d,(I2C_ADDR[0]<<1),INA219_REG[2])
		dataBV = round(float(int(data,16)>>3)*0.004,4)
		logging.debug("Bus Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[0],dataBV))	
		print("Bus Voltage at I2C device addr - 0x%x is %f Volts"%(I2C_ADDR[0],dataBV))	
		#The Second Loop around Temperature Control
		for temp in ESP_Values:
                        Time_Per_Loop = (time.strftime("%H:%M:%S")) + (time.strftime("%d/%m/%Y"))
                        print Time_Per_Loop
                        #Set and Read the Temperature
			espec_setT(temp_chamber,temp)
			time.sleep(100)
			Read_Temperature = espec_readT(temp_chamber)
			print('Temperature Set to %s degree celsius'%Read_Temperature[0])
			logging.debug('Temperature Set to %s degree celsius'%Read_Temperature[0])
				
            #1M Burst Transfer at 1G Speed
			print('Started 1M Burst Transfer at 1G Speed')
			logging.debug('Started 1M Burst Transfer at 1G Speed')
			output = subprocess.check_output('tclsh stc_1000mb.tcl')
			time.sleep(100)
			os.rename('stc_1000mb', 'stc_1000mb_'+str(TPS_Voltage[v])+'_'+temp+'_'+date_str)
			print('Finished 1M Burst Transfer at 1G Speed')
			logging.debug('Finished 1M Burst Transfer at 1G Speed')
			'''
			#100K Burst Transfer at 100M Speed
			print('Started 0.1M Burst Transfer at 100M Speed')
			logging.debug('Started 0.1M Burst Transfer at 100M Speed')
			output = subprocess.check_output('tclsh stc_100mb.tcl')
			time.sleep(100)
			os.rename('stc_100mb', 'stc_100mb_'+str(TPS_Voltage[v])+'_'+temp+'_'+date_str)
			print('Finished 0.1M Burst Transfer at 100M Speed')
			logging.debug('Finished 0.1M Burst Transfer at 100M Speed')

			#10K Burst Transfer at 10M Speed
			print('Started 0.01M Burst Transfer at 1G Speed')
			logging.debug('Started 0.01M Burst Transfer at 10M Speed')
			output = subprocess.check_output('tclsh stc_10mb.tcl')
			time.sleep(100)
			os.rename('stc_10mb', 'stc_10mb_'+str(TPS_Voltage[v])+'_'+temp+'_'+date_str)
			print('Finished 0.1M Burst Transfer at 10M Speed')
			logging.debug('Finished 0.01M Burst Transfer at 10M Speed')
			'''
		logging.debug('Finished 1M Burst Transfer at 1G Speed in all Temperatures at %f Voltage'%TPS_Voltage[v])
		print('Finished 1M Burst Transfer at 1G Speed in all Temperatures at %f Voltage'%TPS_Voltage[v])

espec_chamberoff(temp_chamber)		
logging.debug('Finished 1M Burst Transfer at 1G Speed in all Temperature and in all Voltage Conditions')	
print('Finished 1M Burst Transfer at 1G Speed in all Temperature and in all Voltage Conditions')		
Time_End = (time.strftime("%H:%M:%S")) + (time.strftime("%d/%m/%Y"))
print Time_End
logging.debug(Time_End)
call_ippower('python fence_ip9258.py -a {0} -l {1} -p {2} -n 5 -o off'.format( \
                 IP, login, passwd) \
                ) 
