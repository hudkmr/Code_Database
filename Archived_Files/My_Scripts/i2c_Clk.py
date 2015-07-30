def skClk(rClk,div5,pha3):
	if div5:
		val= float(((60*1000)/(2*rClk))-1)
		if pha3:
			val = val * (2.0/3)
			return hex(int(val))
		else:	
			return hex(int(val))
	else:		
		val= float(((12*1000)/(2*rClk))-1)
		if pha3:
			val = val * (2.0/3)
			return hex(int(val))
		else:	
			return hex(int(val))
			
clk =skClk(2,1,1)			