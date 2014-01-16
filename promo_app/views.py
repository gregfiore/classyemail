from django.shortcuts import render, redirect
from promo_app.models import Email

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

def clean_utf8(input_string):
	if 'utf-8' in input_string:
		return input_string.decode('utf-8')
	else:
		return input_string

def trim_string(og_string, max_length):
	return (og_string[:(max_length-3)] + '...') if len(og_string) > max_length else og_string


def index_view(request):
	args = {}
	args['current_page'] = 'index'
	return render(request, 'index.html', args)

def login(request):
	## Log the user in
	# Need the login form
	return indexview(request)

def home_view(request):
	args = {}
	args['current_page'] = 'home'
	return render(request, 'home.html', args)

def classify_view(request):
	args = {}
	args['current_page'] = 'classify'
	return render(request, 'classify.html', args)

def extract_view(request):
	args = {}
	args['current_page'] = 'extract'
	return render(request, 'extract.html', args)


def all_email_view(request):
	
	args = {}

	# Get all the emails and put them into args
	msgs = Email.objects.all()  # For now just get all emails, later we should filter based on user, date, etc.
	all_emails = []
	for msg in msgs:
		
		sender_data = parse_sender(msg.sender)

		setattr(msg, 'sender', trim_string(sender_data['name'],30))

		new_subject = trim_string(msg.subject,70)
		setattr(msg, 'subject', new_subject)

		all_emails.append(msg)

	args['emails'] = all_emails
	
	args['current_page'] = 'inbox'

	return render(request, 'all_email.html', args)

def email_detail_view(request, email_pk):

	args = {}

	msg = Email.objects.get(pk=email_pk)

	args['email'] = msg

	args['current_page'] = 'email_detail'

	return render(request, 'email_detail.html', args)

