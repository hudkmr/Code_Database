#Simple Script to Switch on and off IP9258 Power Switch
#IP Power Switch 9258 Python Library
import httplib

myURL = '10.64.44.152'
login = 'admin'
passwd = '12345678'
cmd = 'SetPower'
port = 'P61'
ON = '1'
OFF = '0'
args = []

def power_switch_on():
	args.append((port,ON))
	#print args	
	httpconnection = httplib.HTTPConnection(myURL)
	headers = {}
	creds = '%s:%s' % (login, passwd)
	headers['Authorization'] = 'Basic %s' % creds.encode('base64')
	url = '/Set.cmd?CMD=%s' % cmd
	url += ''.join(['+%s=%s' % (k, v) for k,v in args ])
	httpconnection.request('GET', url,headers = headers)
	res = httpconnection.getresponse()
	if res.status != 200:
		print 'Err !!',myURL, 'Seems to be a troublesome URL.'
		print 'The Internet says',res.reason, 'and status',res.status
	else:
		data = res.read()
		allheaders = res.getheaders()
		print'Power Supply Switch On'
		
def power_switch_off():
	args.append((port,OFF))
	#print args	
	httpconnection = httplib.HTTPConnection(myURL)
	headers = {}
	creds = '%s:%s' % (login, passwd)
	headers['Authorization'] = 'Basic %s' % creds.encode('base64')
	url = '/Set.cmd?CMD=%s' % cmd
	url += ''.join(['+%s=%s' % (k, v) for k,v in args ])
	httpconnection.request('GET', url,headers = headers)
	res = httpconnection.getresponse()
	if res.status != 200:
		print 'Err !!',myURL, 'Seems to be a troublesome URL.'
		print 'The Internet says',res.reason, 'and status',res.status
	else:
		data = res.read()
		allheaders = res.getheaders()	
		print'Power Supply Switch Off'
	