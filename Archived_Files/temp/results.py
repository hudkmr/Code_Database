import os,sys
import csv
import shutil

def results_modification(current_mode,result_file,result_folder):
	g_path = '-0001-generatorportresults.csv'
	a_path = '-0002-analyzerportresults.csv'
	r_path = '-0003-rxstreamsummaryresults.csv'
	t_path = '-0004-txstreamresults.csv'
	
	data_folder = os.getcwd() + '\\' + current_mode
	os.chdir(data_folder)

	gf = open((current_mode + g_path),'rb')
	af = open((current_mode + a_path),'rb')
	rf = open((current_mode + r_path),'rb')
	tf = open((current_mode + t_path),'rb')

	final_result = open(result_file,'wb')
	writer = csv.writer(final_result)

	#Adding Generator Port Results
	writer.writerows([['Generator_Results'],''])
	gf_reader = csv.reader(gf)
	writer.writerows(list(gf_reader)[-8:])

	#Adding Analyzing Results
	writer.writerows(['',['Analyzer_Results'],''])
	af_reader = csv.reader(af)
	writer.writerows(list(af_reader)[-8:])

	#Adding RX Stream Results
	writer.writerows(['',['RxStream_Results'],''])
	rf_reader = csv.reader(rf)
	writer.writerows(list(rf_reader)[-8:])

	#Adding TX Stream Results
	writer.writerows(['',['TxStream_Results'],''])
	tf_reader = csv.reader(tf)
	writer.writerows(list(tf_reader)[-8:])
	
	final_result.close()
	
	#Transfering the result 
	destin_file = '..\\'+result_folder+'\\'+result_file
	shutil.copy(result_file,destin_file)
	os.chdir('..//')