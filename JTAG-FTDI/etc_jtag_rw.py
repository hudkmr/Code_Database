from etc_jtag_lib import MPSSE_JTAG
from etc_jtag_lib.etc_header import *
from etc_jtag_lib.etc_jtag_states import *
import time

baudrate = BaudRate(jtag_clk)

dev=MPSSE_JTAG(0)
dev.DevConf(baudrate)

#Set the TAP Controller to Test Logic Reset State
dev.JTAG_Test_Logic_Reset_State()

#Set the TAP Controller to Shift IR State
dev.JTAG_IR_SCAN('07','FF')

#Write 0x30 to IR Register
dev.JTAG_DR_SCAN('07','AA')


