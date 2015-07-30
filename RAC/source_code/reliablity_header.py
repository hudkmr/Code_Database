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

MASTER = 1
SLAVE = 0


#ETC UART Baud Rate
ETC_UART_BAUD = 921600

#Random Burst Size Enable - norm, rad, jumbo
stc_type = 'p11_1_rand_100L'
JUMBO_PACKETS = False
FETL = True

STC_TR_SIZE = ['10','100','1000']
Packet_Size = ['100K','1M','10M']
'''
MIN=1.00
MAX=1.32
STEP=0.02
ANA_TPS_Voltage = []
for i in range(int((MAX-MIN)/STEP)+1):
	ANA_TPS_Voltage += round(MIN+STEP*i,2),

DIG_TPS_Voltage = [1.1]
'''

DIG_TPS_Voltage = [1.072,1.192,1.212]
ANA_TPS_Voltage = [1.072,1.192,1.212]


Temp_C= ['25C']

#Voltage TPS Calculation 
DIG_TPS_Values=[]
for i in DIG_TPS_Voltage:
	DIG_TPS_Values += hex(int((i+0.60)/0.01))[2:] +'00',

#Voltage TPS Calculation 
ANA_TPS_Values=[]
for i in ANA_TPS_Voltage:
	ANA_TPS_Values += hex(int((i+0.60)/0.01))[2:] +'00',	