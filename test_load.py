

import urllib2
import json
import re
import time
from playsound import playsound

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def SendEmail(email_body, email_subject):
	#Function will send the error message to an email address
	fromaddr = from_addr
	
	toaddr = to_addr

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = email_subject
 
	body = email_body
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(fromaddr, pass_email)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.close()


#Load setting file
with open("Settings.txt","r") as file_set:
	setting_data = json.load(file_set)
	
from_addr = str(setting_data['fromaddr'])
to_addr= str(setting_data['toaddr'])
pass_email = str(setting_data['emailpass'])

link_htp = str(setting_data['weblink'])

response = urllib2.urlopen(link_htp)

print response.info()
print response.code

html = response.read()
response.close()

print html

json_result = json.loads(html)

print json_result["row0"][0]["gh_ntemp"]
#print type(json_result["row0"][0]["gh_ntemp"])

#test the json result, see if the temp values are outside of margins
if( float(json_result["row0"][0]["gh_ntemp"]) <  48 ):
	#Below the defined limit
	#Send error msg
	print 'Hit temp. level'
	temp_str = 'North Green House section is below defined limit\n'
	temp_str += 'North Green House Temp:' + str(json_result["row0"][0]["gh_ntemp"])
	temp_str += '\nSouth Green House Temp:' + str(json_result["row0"][0]["gh_stemp"])
	temp_str += '\nControl Green House Temp:' + str(json_result["row0"][0]["con_temp"])
	temp_str += '\nOutside Green House Temp:' + str(json_result["row0"][0]["out_temp"])
	SendEmail(temp_str,'858 temp problem')
	
if( float(json_result["row0"][0]["gh_ntemp"]) >  90 ):
	#Above the defined limit
	#Send error msg
	print 'Hit temp. level'
	temp_str = 'North Green House section is above defined limit\n'
	temp_str += 'North Green House Temp:' + str(json_result["row0"][0]["gh_ntemp"])
	temp_str += '\nSouth Green House Temp:' + str(json_result["row0"][0]["gh_stemp"])
	temp_str += '\nControl Green House Temp:' + str(json_result["row0"][0]["con_temp"])
	temp_str += '\nOutside Green House Temp:' + str(json_result["row0"][0]["out_temp"])
	SendEmail(temp_str,'858 temp problem')
	
	#play sound bit
	playsound('sounds/sound1.mp3')