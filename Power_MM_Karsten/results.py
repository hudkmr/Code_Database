def results_generation(writer,Power_MM,reg_addr,reg_value,description):
	total_power = 0
	for i in range(6):
		total_power += Power_MM[i][4]
		
	#Updating CSV result with Link Speed
	writer.writerows([['Test Condition',description],])
	writer.writerows([['Register','Address','Value'],])
	writer.writerows([['Res_Req Reg',reg_addr,reg_value],])
	writer.writerows(["",['Power Measurement Results',],['ADDR','Config_Reg','Shunt_Voltage','Bus_Voltage','Power','Current','Calibration'],])
	writer.writerows(Power_MM)
	#Adding Generator Port Results
	writer.writerows([['Total Power','','','',str(total_power)],''])	
	
	
