import os,sys
import csv
import shutil
from xlrd import *
from xlutils.copy import copy

def results_xl_file():
	file = copy(open_workbook('..\\results\\final_results.xls'))
	#file.sheet_name('ETC Power Data Transfer Measurements')
	return file
	
def results_file_name(test_condition):
	#CSV file name creation
	file_name ='stc'
	for i in range(len(test_condition)):
		file_name += '_'+test_condition[i]
	return file_name

 
def results_modification(row_no,current_mode,test_condition,result_folder,result_file):
	g_path = '-0001-generatorportresults.csv'
	a_path = '-0002-analyzerportresults.csv'
	r_path = '-0003-rxstreamsummaryresults.csv'
	t_path = '-0004-txstreamresults.csv'
	
	data_folder = os.getcwd() + '\\' + current_mode
	os.chdir(data_folder)

	#CSV file name creation
	csv_file_name = results_file_name(test_condition)+'.csv'
	
	gf = open((current_mode + g_path),'rb')
	af = open((current_mode + a_path),'rb')
	rf = open((current_mode + r_path),'rb')
	tf = open((current_mode + t_path),'rb')

	csv_result = open(csv_file_name,'wb')
	writer = csv.writer(csv_result)
	
	#Creating a Sheet in the Workbook
	res_sheet = result_file.get_sheet(0)
	res_sheet.row(row_no).write(0,row_no)
	
	for i in range(4):
		res_sheet.row(row_no).write((i+1),test_condition[i])
    
	'''
	#Updating CSV result with Link Speed
	writer.writerows([['ETC Port Link Parameters',],''])
	writer.writerows([['PortNo','Firmware Version','Link Speed'],])
	for i in range(5):
		if bin(int(Link[1][i],16))[-2:] == '10':
			writer.writerows([['GPHY'+str(i),Link[0][i],'1000mb'],])
		elif bin(int(Link[1][i],16))[-2:] == '01':	
			writer.writerows([['GPHY'+str(i),Link[0][i],'100mb'],])
		elif bin(int(Link[1][i],16))[-2:] == '00':	
			writer.writerows([['GPHY'+str(i),Link[0][i],'10mb'],])
    '''
	#Adding Generator Port Results
	writer.writerows(['',['Generator_Results'],''])
	gf_reader = csv.reader(gf)
	generator_crc = list(gf_reader)[-8:]
	for i in range(6):
		res_sheet.row(row_no).write((i+11),generator_crc[i+2][20])
	writer.writerows(generator_crc)

	#Adding Analyzing Results
	writer.writerows(['',['Analyzer_Results'],''])
	af_reader = csv.reader(af)
	writer.writerows(list(af_reader)[-8:])

	#Adding RX Stream Results
	writer.writerows(['',['RxStream_Results'],''])
	rf_reader = csv.reader(rf)
	dropped_frame_count = list(rf_reader)[-8:]
	for i in range(6):
		res_sheet.row(row_no).write((i+5),dropped_frame_count[i+2][9])
	writer.writerows(dropped_frame_count)

	#Adding TX Stream Results
	writer.writerows(['',['TxStream_Results'],''])
	tf_reader = csv.reader(tf)
	writer.writerows(list(tf_reader)[-8:])
	
	csv_result.close()
	
	#Transfering the result 
	destin_file = '..\\'+result_folder+'\\'+csv_file_name
	shutil.copy(csv_file_name,destin_file)
	os.chdir('..//')