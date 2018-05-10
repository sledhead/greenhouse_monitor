

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


def Speak_Msg( err_msg, low_or_high ):
	#Function will speak error message by computer speakers.
	
	if( low_or_high == "low" ):
		#play two audio files... One prerecorded
		#for a low temperature condition
		playsound('sounds/low_limit.mp3')
		
	if( low_or_high == "high" ):
		#play two audio files... One prerecorded
		#for a high temperature condition
		playsound('sounds/high_limit.mp3')
		
	time.sleep(10)
	sound_bit = gTTS(err_msg)
	sound_bit.save("sounds/cool.mp3")
	playsound('sounds/cool.mp3')
	#after playing sound file delete
	time.sleep(20)
	os.remove('sounds/cool.mp3')
	print ('sleeping now')
	#Sleep a minute or two before moving ahead
	time.sleep(60)
			
		
#Load setting file
with open("Settings.txt","r") as file_set:
	setting_data = json.load(file_set)
	
from_addr = str(setting_data['fromaddr'])
to_addr= str(setting_data['toaddr'])
pass_email = str(setting_data['emailpass'])

link_htp = str(setting_data['weblink'])

bKeepLooping = True
bLimitLoopTime = False

while( bKeepLooping == True ):

	bWebConnectProblem = False
	bLimitLoopTime = False

	try:
		response = requests.get(link_htp)
		response.raise_for_status()
		
	except requests.exceptions.HTTPError as errh:
		err_msg = 'The server could not fulfill the request. The error code is:' + str(errh)
		SendEmail(err_msg,'979 web server problem')
		bWebConnectProblem = True
	except requests.exceptions.ConnectionError as errc:
		err_msg = 'The server could not fulfill the request. The error code is:' + str(errc)
		SendEmail(err_msg,'979 web server problem')
		bWebConnectProblem = True
	except requests.exceptions.Timeout as errt:
		err_msg = 'The server could not fulfill the request. The error code is:' + str(errt)
		SendEmail(err_msg,'979 web server problem')
		bWebConnectProblem = True
	except requests.exceptions.RequestException as err:
		err_msg = 'The server could not fulfill the request. The error code is:' + str(err)
		SendEmail(err_msg,'979 web server problem')
		bWebConnectProblem = True
	
	else:
		#print response.info()
		print (response.status_code)
		#web_server_code = response.code
		html = response.text
		response.close()

		#check web server response code:
		#print type(web_server_code)
		
	
	if( bWebConnectProblem == False ):
		#print html
		json_result = json.loads(html)

		print (json_result["row0"][0]["gh_ntemp"])
		#print type(json_result["row0"][0]["gh_ntemp"])

		#test the json result, see if the temp values are outside of margins
		if( float(json_result["row0"][0]["gh_ntemp"]) <  48 ):
			#Below the defined limit
			#Send error msg
			print ('Hit temp. level')
			temp_str = 'North Green House section is below defined limit\n'
			temp_str += 'North Green House Temp:' + str(json_result["row0"][0]["gh_ntemp"])
			temp_str += '\nSouth Green House Temp:' + str(json_result["row0"][0]["gh_stemp"])
			temp_str += '\nControl Green House Temp:' + str(json_result["row0"][0]["con_temp"])
			temp_str += '\nOutside Green House Temp:' + str(json_result["row0"][0]["out_temp"])
			SendEmail(temp_str,'858 temp problem')
			
			#Section tells the user what the current temperature is
			audio_str = 'The temperature in the north half of the greenhouse is:' + str(json_result["row0"][0]["gh_ntemp"]) + " degrees."
			audio_str += 'The temperature in the south half of the greenhouse is:' + str(json_result["row0"][0]["gh_stemp"]) + " degrees."
			audio_str += 'The Control Box temperature is:' + str(json_result["row0"][0]["con_temp"]) + " degrees."
			
			Speak_Msg( audio_str , "low" )
			
		if( float(json_result["row0"][0]["gh_ntemp"]) >  90 ):
			#Above the defined limit
			#Send error msg
			print ('Hit temp. level')
			temp_str = 'North Green House section is above defined limit\n'
			temp_str += 'North Green House Temp:' + str(json_result["row0"][0]["gh_ntemp"])
			temp_str += '\nSouth Green House Temp:' + str(json_result["row0"][0]["gh_stemp"])
			temp_str += '\nControl Green House Temp:' + str(json_result["row0"][0]["con_temp"])
			temp_str += '\nOutside Green House Temp:' + str(json_result["row0"][0]["out_temp"])
			SendEmail(temp_str,'858 temp problem')
			
			#Section tells the user what the current temperature is
			audio_str = 'The temperature in the north half of the greenhouse is:' + str(json_result["row0"][0]["gh_ntemp"]) + " degrees."
			audio_str += 'The temperature in the south half of the greenhouse is:' + str(json_result["row0"][0]["gh_stemp"]) + " degrees."
			audio_str += 'The Control Box temperature is:' + str(json_result["row0"][0]["con_temp"]) + " degrees."
			
			Speak_Msg( audio_str , "high" )
			#play sound bit
			#playsound('sounds/i-dock.mp3')
			
			#When high temp limit has been reached
			#set flag so that we check more often and play WARNING
			#sound more often
			bLimitLoopTime = True

		#Sleep a minute or two before moving ahead
		print ("begin layover")
		if( bLimitLoopTime == True ):
			#sleep for less time
			
			time.sleep(60)
		else:
			time.sleep(180)
			
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
		print ("Some connection problems")

