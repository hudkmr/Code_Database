#Python Script to Read the Inverse Rom Code
#Find the length of the hex file	
#!/usr/bin/python
import sys
	
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
	
#Enter the File name
if len(sys.argv) > 1:
	hex_file = sys.argv[1]
	noce = file_len(hex_file) -1	
	f_inp = open(hex_file)
	f_inp_lines = f_inp.readlines()
	f_out = open(hex_file[:-4]+'_inv.hex','wb')
	count = 10
	while (noce >= 0):
		temp = f_inp_lines[noce]
		f_out.write(temp)
		if temp == 'ffff\n':
			count= count -1
		noce = noce -1
		if count == 0:
			break
	
	f_out.close()
	f_inp.close()
else:
	print 'Enter the proper hexfile for conversion'
	

	