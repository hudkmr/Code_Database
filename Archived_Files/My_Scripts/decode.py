def decode_fun(data):
      for char in data:
			data = '0' + char
			print data
			print data.decode('hex')
			