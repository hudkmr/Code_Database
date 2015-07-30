import multiprocessing
import time
import sys
import subprocess

def stc_data():
    print 'Starting:', multiprocessing.current_process().name
    time.sleep(10)
    print 'Exiting :', multiprocessing.current_process().name

def power_mm():
    print 'Starting:', multiprocessing.current_process().name
    print 'Exiting :', multiprocessing.current_process().name

if __name__ == '__main__':
	d = multiprocessing.Process(name='stc_data', target=stc_data)
	d.daemon = True

	n = multiprocessing.Process(name='power_mm', target=power_mm)
	n.daemon = False

	d.start()
	n.start()

	n.join()
	print 'd.is_alive()', d.is_alive()
	d.join()
	print 'd.is_alive()', d.is_alive()