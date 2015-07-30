# ----------
# import the Pyserial module
import time
import sys
#if "K:\4_CPRJ\ETC\python\etc_py_libs" not in sys.path:
#    sys.path.append("K:\4_CPRJ\ETC\python\etc_py_libs")

import ssb_fast_lib

def etc_flashdwnld(com_port,hex_file):

     #"""   ------------------------------------------------------------------------------------------- """
     #"""                              Set-up the COM port                                              """
     #"""   ------------------------------------------------------------------------------------------- """
     pp = flash_dwnld.etcFlash(com_port) # open port COM10
     #pp = flash_dwnld.etcFlash(10)
     ########################################################################################################
     #                                BEGIN
     ########################################################################################################

     #
     start_time = time.time()

     # Open the Flash hex file
     #f = open('d:\\Code\\etc_flash.hex')
     f  = open (hex_file)

     # Erase Flash
     pp.flash_erase()

     start_time = time.time()
	 
     #Program The Flash
     pp.flash_down_ld(f)

     

     #Verify if the Download is successful	 
     check = pp.check_dwnld()
	 
     elapsed_time = time.time() - start_time
	 
     if check == 1:
          print "\nDownload Successful , in seconds: ", str(elapsed_time)
     else:
	     print "\n Download is NOT successful"
     
     #Close the Port
     pp.close()
     #
     #
     #
print "Flash Download Programe is initiated"
print "Ensure the COMPORT is free"
comport = int(raw_input('Enter the Com port no:'))
hexfile = raw_input('Enter the hex file to be copied to flash memory:')
etc_flashdwnld(comport,hexfile)