import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders


EMAIL_FROM = "h.udayakumar.ee@lantiq.com"
EMAIL_TO = "h.udayakumar.ee@lantiq.com"
EMAIL_CC = ""
SUBJECT = "Performance Results"
username = 'udayakum'
password = 'Bangalore@2014'

def send_mail(result_file,test_condition):
	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT 
	msg['From'] = EMAIL_FROM
	msg['To'] = EMAIL_TO
	msg['Cc'] = EMAIL_CC
	EMAIL_LIST = [EMAIL_TO] + [EMAIL_CC]
	filepath = "..\\results\\" + result_file
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filepath, "rb").read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment', filename=result_file)
	msg.attach(part)

	# Create the body of the message (a plain-text and an HTML version).
	text = ("""Hi Ban Hok,		
			\nPlease find the attached Reliability/Performance Test Results.\n
			\nTest Condition:-
			1.DUT Used - %s
			2.Cable Length - %s
			3.Date and Time - %s
			\nRegards,
			\nHari
		   """%(test_condition[0],test_condition[1],test_condition[2]))
		   
	part1 = MIMEText(text, 'plain')
	msg.attach(part1)
	
	server = smtplib.SMTP('outlook01.lantiq.com',25)
	server.starttls()
	server.login(username,password)
	server.sendmail(EMAIL_FROM, EMAIL_LIST, msg.as_string())