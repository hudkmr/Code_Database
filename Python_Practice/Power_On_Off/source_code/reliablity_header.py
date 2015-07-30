#This Script Contains Parameter Required for Reliablity Testcase 
#List of Python Library Required

import time
from datetime import *
import os
import sys
import logging
import shutil 

#ETC Ports
ETC_UART0 = 0
ETC_UART1 = 1
ETC_UART2 = 2
ETC_UART3 = 3

#ETC UART Baud Rate
ETC_UART_BAUD = 921600

#Random Burst Size Enable
rad=False 
FETL=False
FULL_DUPLEX = True

STC_TR_SIZE = ['1000']
Packet_Size = ['10M','1M','100K']

TPS_Voltage = [1.1,1.045,1.155]
Temp_C= ['S25']

#Voltage TPS Calculation 
TPS_Values=[]
for i in TPS_Voltage:
	TPS_Values += hex(int((i+0.60)/0.01))[2:] +'00',
	