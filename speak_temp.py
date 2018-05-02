

import requests
from gtts import gTTS
import json
import re
import time
from playsound import playsound
import os


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


response = requests.get(link_htp)

html = response
response.close()

print (html.status_code)

json_result = json.loads(html.text)

print (json_result["row0"][0]["gh_ntemp"])
#print type(json_result["row0"][0]["gh_ntemp"])

#test the json result, see if the temp values are outside of margins


temp_str = 'The temperature in the north half of the greenhouse is:' + str(json_result["row0"][0]["gh_ntemp"]) + " degrees."
temp_str += 'The temperature in the south half of the greenhouse is:' + str(json_result["row0"][0]["gh_stemp"]) + " degrees."
temp_str += 'The Control Box temperature is:' + str(json_result["row0"][0]["con_temp"]) + " degrees."

#print (temp_str)
#sound_bit = gTTS(temp_str)
#sound_bit.save("cool.mp3")

bKeepLooping = True
bLimitLoopTime = False

while( bKeepLooping == True ):

	bWebConnectProblem = False
	bLimitLoopTime = False

	
	response = requests.get(link_htp)

	html = response
	response.close()

		
	
	if( bWebConnectProblem == False ):
		#print html
		json_result = json.loads(html.text)

		print (json_result["row0"][0]["gh_ntemp"])
		#print type(json_result["row0"][0]["gh_ntemp"])

		#test the json result, see if the temp values are outside of margins
		temp_str = 'The temperature in the north half of the greenhouse is:' + str(json_result["row0"][0]["gh_ntemp"]) + " degrees."
		temp_str += 'The temperature in the south half of the greenhouse is:' + str(json_result["row0"][0]["gh_stemp"]) + " degrees."
		temp_str += 'The Control Box temperature is:' + str(json_result["row0"][0]["con_temp"]) + " degrees."
		
		sound_bit = gTTS(temp_str)
		sound_bit.save("sounds/cool.mp3")
		playsound('sounds/cool.mp3')
		#after playing sound file delete
		time.sleep(20)
		os.remove('sounds/cool.mp3')
		print ('sleeping now')
		#Sleep a minute or two before moving ahead
		time.sleep(120)
			
		print ('done sleeping')

		#Before beginning the loop again, see if user wants to end program
		setting_file = open('Gather.txt','r')
		single_line = setting_file.readline()
		setting_file.close()

		run_status = re.search(r'no',single_line,re.M|re.I)
		if(run_status):
			#User set line to no, quit running program
			print ('Stopping program execution')
			bKeepLooping = False
	else:
		time.sleep(180)	
#play sound bit
#playsound('sounds/sound1.mp3')