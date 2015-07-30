import multiprocessing
import time
import sys
import subprocess
from etc_main import *

def stc_data():
    print 'Starting:', multiprocessing.current_process().name
    subprocess.check_output('tclsh stc_1000mb.tcl')
    print 'Exiting :', multiprocessing.current_process().name

def power_mm():
	print 'Starting:', multiprocessing.current_process().name
	etc_main()
	print 'Exiting :', multiprocessing.current_process().name

if __name__ == '__main__':
	d = multiprocessing.Process(name='stc_data', target=stc_data)
	d.daemon = True

	n = multiprocessing.Process(name='power_mm', target=power_mm)
	n.daemon = False

	d.start()
	time.sleep(30)
	n.start()

	n.join()
	print 'd.is_alive()', d.is_alive()
	d.join()
	print 'd.is_alive()', d.is_alive()