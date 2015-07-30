This script measures Power measurements wrt various conditions mentioned in the input.txt file
To Execute this script we pass the input.txt and "Output File name" in the command line along with
Actual python script "etc_i2c_ina219_EIF.py"

example -
python etc_i2c_ina219_EIF.py input.txt output_file_name


In order add more testcase modify the input.txt file
Sl.no No_write commands Reg_Addr_1 Reg_data_1 ... Description comment
if your no_write commands is 0 no write to internal register are performed
if your no_write commands is non-zero ensure the reg address and data are there, follow the previous pattern


-Regards
Hari
