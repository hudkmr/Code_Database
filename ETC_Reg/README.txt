This Script logs the register dump values using ETC port
Three Parameters are passed to scripts
1. Output File Name
2. Register Start Address - in Hex Format
3. Register End Address - in Hex Format

Example:-
	python etc_reg_log.py Register_Log 0xFA00 0xFAFF
	           |						|		|
			   |					|		|	
			   |						|		|
			   V						|		|
			   python script			V		|
								  Start Address	|
												|
												V
											Destination Address