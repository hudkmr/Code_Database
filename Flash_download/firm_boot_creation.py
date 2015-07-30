#Python Script to Read the Inverse Rom Code
#Find the length of the hex file		
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
	
#Enter the Firmware File
firm_file=raw_input('Enter the firmware file:')
firm_noce = file_len(firm_file) -1					#Read the no of lines in Firmware File
firm_inp = open(firm_file)						    #Open Firmware File
firm_inp_lines = firm_inp.readlines()				#Read the lines of Firmware File

#Open Bootcode file
boot_file=raw_input('Enter the Bootcode file:')
boot_noce = file_len(boot_file) -1					#Read the no of lines in Firmware File
boot_inp = open(boot_file)						#Open Firmware File
boot_inp_lines = boot_inp.readlines()				#Read the lines of Firmware File

i=0
break_count =0
while(i < 30720):
	firm_line = firm_inp_lines[i]
	boot_inp_lines[i] = firm_line
	i = i + 1
		
#Creating Firmware + Bootcode File
firm_boot_out = open('firm_boot_code.hex','wb')
firm_boot_out.writelines(boot_inp_lines)
firm_boot_out.close()
firm_inp.close()
boot_inp.close()
	