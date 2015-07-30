import os,sys
import csv

def results_modification(current_mode,rename):
	print current_mode,rename
	g_path = '-0001-generatorportresults.csv'
	a_path = '-0002-analyzerportresults.csv'
	r_path = '-0003-rxstreamsummaryresults.csv'
	t_path = '-0004-txstreamresults.csv'
	
	result_folder = os.getcwd() + '\\' + current_mode
	os.chdir(result_folder)

	gf = open((current_mode + g_path),'rb')
	af = open((current_mode + a_path),'rb')
	rf = open((current_mode + r_path),'rb')
	tf = open((current_mode + t_path),'rb')

	final_result = open(current_mode + rename +'.csv','wb')
	writer = csv.writer(final_result)

	#Adding Generator Port Results
	writer.writerows([['Generator_Results'],''])
	reader = csv.reader(gf)
	writer.writerows(list(reader)[-8:])

	#Adding Analyzing Results
	writer.writerows(['',['Analyzer_Results'],''])
	reader = csv.reader(af)
	writer.writerows(list(reader)[-8:])

	#Adding RX Stream Results
	writer.writerows(['',['RxStream_Results'],''])
	reader = csv.reader(rf)
	writer.writerows(list(reader)[-8:])

	#Adding RX Stream Results
	writer.writerows(['',['TxStream_Results'],''])
	reader = csv.reader(tf)
	writer.writerows(list(reader)[-8:])

