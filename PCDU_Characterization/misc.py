#Miscellaneous Functions
import time

def current_time():
	return time.strftime("%d%H%M")
	
def int_to_str(val):
	temp = hex(val)[2:]
	while len(temp) < 4:
		temp = '0'+temp
	return temp