#Find the no of Matchin letter in string
string1 = raw_input('Enter a String 1:')
string2 = raw_input('Enter a String 2:')
i=0;
string1_match=0
while(i < len(string1)):
	for j in range(i+1, len(string1)):
		print i,string1[i],j,string1[j]
		if string1[i] == string1[j]:
			string1_match = string1_match + 1
	i = i +1	
	print string1_match