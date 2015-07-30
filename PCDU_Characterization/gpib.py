#*****************************************************
## Authour: Sudhakar Sayana
## GPIB utility functions
#*****************************************************

import visa;
import time;
import serial;

def serial_init(port="COM1",baudrate=19200):
    return serial.Serial(port,baudrate,timeout=0)

def gpib_init(ins="GPIB0::0"):
    return visa.instrument(ins)

def espec_chamberoff(ins):
    ins.write("01,POWER,OFF\r")

def espec_chamberon(ins):
    ins.write("01,POWER,ON\r")

def espec_setT(ins, temp):
      ins.write("01,TEMP,S%s\r"%temp)
	  
def espec_readT(ins):
	ins.write("01,TEMP?\r")
	ReadT=ins.read()
	return ReadT
      
def espec_waitT(ins):
    from string import rsplit
    buf = ins.readlines();
    time.sleep(2)
    ins.write("1,TEMP?\r")
    time.sleep(2)
    buf = ins.readlines();
    temp = buf[0].split(',',4)
    print float(temp[0])
    print float(temp[1])
    if abs(float(temp[1]) - float(temp[0])) < 1.0:
        print "Temperature is set"
        return 0
    else:
        time.sleep(120)
        espec_waitT(ins)              

def chamberoff(ins):
    ins.write("01,POWER,OFF")

def chamberon(ins):
    ins.write("01,POWER,ON")

def setT(ins,temp=25):
    ins.write("01,TEMP,S{temp} H90 L-40".format(temp=temp))

def setH(ins,humidity=0):
    ins.write("01,HUMI,S{humidity} H10 L0".format(humidity=humidity))

def waitT(ins):
    ins.write("01,TEMP?")
    temp = ins.read();
    temp = temp.split(',',4)
    print float(temp[0])
    print float(temp[1])
    if abs(float(temp[1]) - float(temp[0])) < 1.0:
        print "Temperature is set"
        return 0
    else:
        time.sleep(120)
        waitT(ins)              
    
def clear(ins):
    ins.write("*CLS")

def reset(ins):
    ins.write("*RST")

def set6v(ins,voltage=1.000,current=1.000):
    ins.write("APPLY P6V, {voltage}, {current}".format(voltage=voltage,current=current))
 
def set25v(ins,voltage=1.000,current=1.000):
    ins.write("APPLY P25V, {voltage}, {current}".format(voltage=voltage,current=current))

def poweron(ins):
    ins.write("OUTPUT:STATE ON")

def poweroff(ins):
    ins.write("OUTPUT:STATE OFF")

def checkCurrents(ins):
    ins.write("MEASURE:CURRENT:DC? P6V")
    print "6V Current is: ", ins.read();
    ins.write("MEASURE:CURRENT:DC? P25V")
    print "25V Current is: ", ins.read();

def checkVoltages(ins):
    ins.write("MEASURE:VOLTAGE:DC? P6V")
    print "6V Voltage is: ", ins.read();
    ins.write("MEASURE:VOLTAGE:DC? P25V")
    print "25V Voltage is: ", ins.read();

def measureV(ins):
    ins.write("*CLS")
    ins.write("*RST");
    f = open("C:\\voltage.txt",'w');
    ins.write("MEASURE:VOLTAGE:DC? 10,0.003");
    voltage = ins.read();
    print "voltage is:", voltage
    f.write(str(voltage));
    f.flush();
    f.close();
