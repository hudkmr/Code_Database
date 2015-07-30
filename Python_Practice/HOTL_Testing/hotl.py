import time
import visa

print('HOTL Testing for 34 Hours')
print('start time -'),time.strftime("%d-%m-%y %H:%M:%S")
stress_time = 34*60*60
timeout = time.time() + stress_time   # 34 Hours from now
temp = visa.instrument("GPIB0::0")
temp.write('01,POWER,ON\r')
temp.write('01,TEMP,S80\r')
while True:
    test = 0
    if time.time() > timeout:
        break
    #test = test - 1
print('END time -'),time.strftime("%d-%m-%y %H:%M:%S")
temp.write('01,POWER,OFF\r')
print('HOTL Testing Completed')
