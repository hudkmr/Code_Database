#Python Script to Read the Inverse Rom Code
#Find the length of the hex file		
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
	
#Enter the File name
firm_file=raw_input('Enter the firmware file:')
boot_file=raw_input('Enter the bootcode file:')
noce = file_len(hex_file) -1	
f_inp = open(hex_file)
f_inp_lines = f_inp.readlines()
f_out = open(hex_file[:-4]+'_inv.hex','wb')
while (noce >= 0):
	f_out.write(f_inp_lines[noce])
	noce = noce -1
	
f_out.close()
f_inp.close()
	

	