#!/usr/bin/env python

##############################################
# EMXL wrapper                               # 
# ------------------------------------------ #
# Purpose:    Recursively searches for .emlx #
#             files                          #
# Name:       get_emlx(arg)                  #
# Input(s):   Directory name <string>        #
# Output(s):  List of .emlx files with paths #
##############################################

############################
# Python modules to import #
############################
import os
import sys

#################################
# Search for files in directory #
#################################

def get_emlx(search_dir):
	# Initialize the list of filenames as empty
	filenames = []

	for root, dirname, files in os.walk(search_dir):
		for file in files:
			if 'Attachments' not in root and '.emlx' in file and '.partial.' not in file and 'emlxpart' not in file:
				filenames.append(root + '/' + file)

	return filenames

##############################################
# EMXL extractor                             # 
# ------------------------------------------ #
# Purpose:    Extract components from email  #
# Name:       extract_emlx(arg)              #
# Input(s):   Filename name <string>         #
# Output(s):  Dictionary of email components #
##############################################

############################
# Python modules to import #
############################

import email
from email.parser import Parser

#############################
# Open and extract the file #
#############################

def extract_emlx(filename):

	data = {'id':'', 'date':'', 'to':'', 'from':'', 'subject':'', 'body':{'plain':'', 'html':''}}
	try:
		fh = open(filename,'rb')
	except:
		print 'Error opening file in extract_emlx: ' + filename
		return 0

	# get the payload length
	bytes = fh.readline().strip()
	# get the MIME payload
	message = email.message_from_string(fh.read(int(bytes)))
	# the remaining bytes are the .plist
	plist = ''.join(fh.readlines())  # This is currently ignored
	# Close the file
	fh.close()

	# Put the appropriate 
	data['id'] = message['message-id']
	data['date'] = message['date']
	data['subject'] = message['subject']
	data['from'] = message['from']
	data['to'] = message['to']

	if message.is_multipart():
		# Most messages are multipart (i.e. plain text and html at least)
		for part in message.get_payload():
			if 'text/plain' in part.get_content_type():
				data['body']['plain'] = str(part)
			elif 'text/html' in part.get_content_type():
				data['body']['html'] = str(part)
	
	else:
		if 'text/plain' in message.get_content_type():
			data['body']['plain'] = str(message.get_payload())
		elif 'text/html' in message.get_content_type():
			data['body']['html'] = str(message.get_payload())

	return data
	