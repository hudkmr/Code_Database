import csv

pwr_mm = open('result.csv','wb')
writer = csv.writer(pwr_mm)

writer.writerows([['ADDR','Config_Reg','Shunt_Voltage','Bus_Voltage','Power','Current','Calibration'],])

pwr_mm.close()