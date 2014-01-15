#!/usr/bin/env python

#####################################################
# Preprocess email                                  # 
# ------------------------------------------------- #
# Purpose:    Preprocess email for classification   #
# by extracting key word/criteria                   #
# Name:       preprocess_emaoil(arg)                #
# Input(s):   Email content <dictionary>            #
# Output(s):  Dictionary of preprocessed attributes #
#####################################################

############################
# Python modules to import #
############################

import email
import re

#####################
# Utility functions #
#####################

def parse_sender(sender):
	##############################################
	# Function: parse_sender(sender)             #
	# Input:  sender of email <string>           #
	# Output:  dictionary of name, address       #
	##############################################

	output = {'name':'', 'address':''}
	# Sender has the following format 'name' <'address'>

	a = email.utils.parseaddr(sender)
	# parseaddr returns 
	output['name'] = a[0]
	output['address'] = a[1]

	return output

def recipient_status(recipient, user_email):
	#########################################################
	# Function: recipient_status(recipient, user_email)     #
	# Input:    recipient <string or list>                  #
	#           user_email user email addresses <list>      #
	# Output:   1 or 0 depending on if the user is a direct # 
	#		    recipient of the email                      #
	#########################################################
	for account in user_email:
		# Check each account to see if they're the recipient
		if recipient:
			if account.lower() in recipient.lower():
				# If so, set the flag to 1
				return 1

	return 0

def set_common_words():
	##############################################
	# Function: set_common_words()		         #
	# Input:  None					             #
	# Output:  None					             #
	##############################################
	# common_words is a global variable

	global common_words
	common_words = []
	fh = open('common_words.txt','r')
	n_words = 20  # Number of words in the list to use
	cnt = 1
	for line in fh:
		if cnt > n_words:
			break
		else:
			# split by period
			a = line.split('.')
			common_words.append(a[1].lower().strip())
		cnt += 1

	return


def parse_subject(subject):
	##############################################
	# Function: parse_subject(subject)           #
	# Input:  subject of email <string>          #
	# Output:  list of key words in the subject  #
	##############################################

	output = {'words':[],'%': 0}  # initialize the output list

	# Check if common words exists, otherwise create it
	if 'common_words' not in globals():
		print 'Initializing common words'  # For debugging to make sure it doesn't occur excessively
		set_common_words()
		print common_words

	subject_words = subject.split()
	bad_chars = '[!@#]*=-()+&@'

	for word in subject_words:
		for i in range(0, len(bad_chars)):
			word = word.replace(bad_chars[i],'')
		if word.lower() not in common_words and len(word) > 0:
			# For now, not looking for duplicates, but this could be an issue
			output['words'].append(word.lower())
		if '%' in word:
			output['%'] = 1

	return output

#################################
# Search for files in directory #
#################################

def preprocess_email(email_data, user_email):
	# Define dictionary of preprocessed attributes (output)
	# Sender:  name, address
	# Recipient:  Does this make sense? - would be personalized to the individual user 
	#             **Just do a flag for if its the user**
	# Subject:  break out key words (i.e. remove common words)
	output = {
		'sender':{'name':'', 'address':''},
		'recipient':0,
		'subject':{},
	}

	# Parse the sender
	output['sender'] = parse_sender(email_data['from'])

	# Flag the recipient
	output['recipient'] = recipient_status(email_data['to'], user_email)

	# Parse the subject
	output['subject'] = parse_subject(email_data['subject'])

	return output
