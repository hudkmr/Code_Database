from xlsxwriter import *

#Creating the excel sheet
def creating_xl_file(filename):
	w = Workbook(filename)
	return w

def creating_xl_sheet(workbook):
	w_s1 = workbook.add_worksheet()
	w_s2 = workbook.add_worksheet()
	return w_s1
	
def ws_header(w_sheet,no_of_tries):
	w_sheet.write(0,0,'Sl.no')
	w_sheet.write(0,1,'Description')
	w_sheet.write(0,2,'Avg Power from %d tries'%(no_of_tries))
	for i in range(no_of_tries):
		w_sheet.write(0,(3+(i*6)),'Overall Power - %d'%(i+1))
		w_sheet.write(0,(4+(i*6)),'Power 3.3v Analog')
		w_sheet.write(0,(5+(i*6)),'Power 1.1v Analog')
		w_sheet.write(0,(6+(i*6)),'Power 1.1v Digital')
		w_sheet.write(0,(7+(i*6)),'Current 3.3v Analog')
		w_sheet.write(0,(8+(i*6)),'Current 1.1v Analog')
		w_sheet.write(0,(9+(i*6)),'Current 1.1v Digital')

def add_mm_ws(w_sheet,row_no,description,power_mm,no_of_tries):
	w_sheet.write(row_no,0,row_no)
	w_sheet.write(row_no,1,description)
	w_sheet.write(row_no,2,'=AVERAGE(D%s,J%s,P%s)'%(row_no+1,row_no+1,row_no+1))
	for i in range(no_of_tries):
		overall_power = power_mm[i][0][4] + power_mm[i][2][4] + power_mm[i][3][4]
		w_sheet.write(row_no,(3+(i*6)),overall_power)
		w_sheet.write(row_no,(4+(i*6)),power_mm[i][2][4])
		w_sheet.write(row_no,(5+(i*6)),power_mm[i][0][4])
		w_sheet.write(row_no,(6+(i*6)),power_mm[i][3][4])
		w_sheet.write(row_no,(7+(i*6)),power_mm[i][2][5])
		w_sheet.write(row_no,(8+(i*6)),power_mm[i][0][5])
		w_sheet.write(row_no,(9+(i*6)),power_mm[i][0][5])