#!/usr/bin/python
from etc_uart import *
import os,sys
import csv
import shutil
import sys


# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
b_rate = int(form.getvalue('baud_rate'))
s_addr = int(form.getvalue('start_address'),16)
e_addr  = int(form.getvalue('end_address'),16)
o_filename = form.getvalue('output_file_name')

commands = sys.argv

#Log CSV File for ETC Register Values
csv_file_name = 'ETC_Register_Log_'+o_filename+'.csv'
csv_result = open(csv_file_name,'wb')
writer = csv.writer(csv_result)

#Updating CSV result with Link Speed
writer.writerows([['ETC Registers',],''])
writer.writerows([['Sl.no','Register Address','Value'],])

#Open UART 1 
uart = uart_reg_rw(1,b_rate)

for i in range(s_addr,e_addr):
	sl_no = str(i-s_addr+1)
	addr  = hex(i)[2:]
	data  = '0x'+uart.gphy_rd(hex(i)[2:])
	print data
	writer.writerows([[sl_no,addr,data],])
	
csv_result.close()	
uart.gphy_close()
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>ETC Register Dump Script Output</title>"
print "</head>"
print "<body>"
print "<h1>ETC Register Dump Output Completed</h1>" 
print "<h2>Result file - %s</h2>"%(o_filename)
print "</body>"
print "</html>"


