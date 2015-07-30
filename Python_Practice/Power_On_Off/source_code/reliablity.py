#----------------------------------------------------------------------------------------------------------
#This Script Automates the Reliablitiy testing for ETC 
#Voltage Modification - 1.1V,1.045, 1.055  #Temperature Modification - 0C, 25C, 75C 
from reliablity_header 	import *
from ps_main import *
from etc_uart import *
from etc_ftdi_main import *
from stc_data_transfer import *

#Loggind Debug Information Time Stamp
date=date.today()
date_str=time.strftime("%d-%m-%y_%H-%M-%S") 

#Cable Length Input
dut = raw_input("Enter the Device under test/Sample Type:") 
cable_length = raw_input("Enter the cable length used for data transfer:")
result_folder = '..\\results\\STC_'+ cable_length +'_Results_'+ date_str
os.mkdir(result_folder)
xl_result_file =  results_xl_file()
test_inputs = [dut,cable_length,date_str]

row_no = 1
#First Loop for various Temperature
for power_on_off_loop in range(50):
	print('Started Power on off Test %d Temperature'%power_on_off_loop)
	#Switching on IP Power Switch Port No 2  
	power_switch_on() 
	time.sleep(30)

	#Initialize GPHY_UART Port no 2 and Enable all Switch Port
	#uart_port = uart_reg_rw(ETC_UART1,ETC_UART_BAUD)
	#gphy_enable(uart_port)
			
	#Fourth Loop  STC Burst Size
	test_condition = []
	st_size= 0
	#Setting the GPHY Port Link Speed
	test_condition += STC_TR_SIZE[st_size],Packet_Size[st_size],str(power_on_off_loop),cable_length
	print('Started Burst Transfer at %smbps Speed'%STC_TR_SIZE[st_size])
	data_transfer(row_no,STC_TR_SIZE[st_size],rad,test_condition,result_folder,xl_result_file)
	row_no += 1
	print('Finished Burst Transfer at %smbps Speed'%STC_TR_SIZE[st_size])
	power_switch_off()	
	time.sleep(10)
	
print('Finished stc_data_transfer in all temperature')	
final_result_file = results_file_name(test_inputs)+'.xls'
xl_result_file.save('..\\results\\'+final_result_file)
power_switch_off() 

		
