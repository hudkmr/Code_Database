#----------------------------------------------------------------------------------------------------------
#This Script Automates the Reliablitiy testing for ETC 
#Voltage Modification - 1.1V,1.045, 1.055  #Temperature Modification - 0C, 25C, 75C 
from reliablity_header_brd2 	import *
from ps_main_brd2 import *
from etc_uart import *
from etc_ftdi_main_brd2 import *
from stc_data_transfer_brd2 import *
from rac_email_brd2 import *
import os

#Switching on IP Power Switch Port No 2  
power_switch_on() 
time.sleep(20)
digital_voltage_loop_len = len(DIG_TPS_Values)
analog_voltage_loop_len = len(ANA_TPS_Values)
#print digital_voltage_loop_len,analog_voltage_loop_len
print DIG_TPS_Voltage
print ANA_TPS_Voltage

#Initialize GPHY_UART Port no 2 and Enable all Switch Port
uart_port = uart_reg_rw(2,ETC_UART_BAUD)
gphy_enable(uart_port)

#Enable FETL Mode
if FETL == True:
	etc_fetl(uart_port)
	
#Jumbo Packets 
if JUMBO_PACKETS == True:
		etc_jumbo(uart_port)
	
#Loggind Debug Information Time Stamp
date=date.today()
date_str=time.strftime("%d-%m-%y_%H-%M-%S") 

#Cable Length Input
dut = raw_input("Enter the Device under test/Sample Type:") 
cable_length = raw_input("Enter the cable length used for data transfer:")
result_folder = '..\\results\\STC_'+ dut +'_'+cable_length +'_Results_'+ date_str
os.mkdir(result_folder)
xl_result_file =  results_xl_file()
test_inputs = [dut,cable_length,date_str]

#Initialize FTDI I2C Port and Configuring Slave I2C CSM's Calibration Register
i2c_dev=etc_main(0)
i2c_dev.etc_i2c_init()

row_no = 1
#First Loop for various Temperature
for temp_loop in Temp_C:
	print('Started Burst Transfer at %s Temperature'%temp_loop)
	
	#The Second Loop is around voltage source 1(digital)
	for av in range(analog_voltage_loop_len):
		data_av = i2c_dev.etc_ana_mod(ANA_TPS_Values[av])
		print("Analog 1.1V set to %f volts"%data_av)	
		
		#Third Loop - is around voltage source 2(analog)
		for dv in range(digital_voltage_loop_len):
			data_dv = i2c_dev.etc_dig_mod(DIG_TPS_Values[dv])
			print("Digital 1.1V set to %f volts"%data_dv)
			
			#Fourth Loop  STC Burst Size
			for st_size in range(len(STC_TR_SIZE)):
				test_condition = []
				#Setting the GPHY Port Link Speed
				test_condition += dut,STC_TR_SIZE[st_size],Packet_Size[st_size],temp_loop,cable_length,str(DIG_TPS_Voltage[dv]),str(ANA_TPS_Voltage[av])
				print('Started Burst Transfer at %smbps Speed'%STC_TR_SIZE[st_size])
				data_transfer(row_no,STC_TR_SIZE[st_size],i2c_dev,uart_port,test_condition,result_folder,xl_result_file,stc_type)
				row_no += 1
				print('Finished Burst Transfer at %smbps Speed'%STC_TR_SIZE[st_size])
			print('Finished Data Transfer at all Burst size')
		
		print('Finished Data Transfer at all  Digital voltage Condition with analog Voltage at:%f'%DIG_TPS_Voltage[dv])			
			
	print('Finished Burst Transfer in all Analog Voltage Condition')			
	print('Finished STC data transfer at %s temperature in all Burst size'%temp_loop)

print('Finished stc_data_transfer in all temperature')	
#Save Result Log
final_result_file = results_file_name(test_inputs)+'.xls'
xl_result_file.save('..\\results\\'+final_result_file)

#Send mail with result attachment
send_mail(final_result_file,test_inputs)

#Close the Device Connection and Turnoff the Power Switch
i2c_dev.Close()
power_switch_off() 



		
