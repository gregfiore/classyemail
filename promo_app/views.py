from django.shortcuts import render, redirect, render_to_response
from promo_app.models import Email
from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import email
import re
import mailbox

#####################
# Utility functions #
#####################

def get_message_parts(msg_payload):
	if msg_payload.is_multipart() and len(msg_payload.get_payload()) == 1:
		# This is a corner case where the plain/html are embedded an additional layer down
		return get_message_parts(msg_payload.get_payload()[0])
	else:
		output = {'plain':'', 'html':''}

		if msg_payload.is_multipart():
			# Now assume it is of length 2 (html and plain text)
			for part in msg_payload.get_payload():
				if 'text/plain' in part.get_content_type():
					output['plain'] = part.get_payload(decode=True)
				elif 'text/html' in part.get_content_type():
					output['html'] = part.get_payload(decode=True)
		else:
			if 'text/plain' in msg_payload.get_content_type():
				output['plain'] = msg_payload.get_payload(decode=True)
			elif 'text/html' in msg_payload.get_content_type():
				output['html'] = msg_payload.get_payload(decode=True)

		return output

def retrieve_body(msg):
	# Input is an Email object
	mbox = mailbox.mbox(msg.email_source)
	full_msg = mbox.get(msg.email_key)

	output = {'plain':'', 'html':''}

	output = get_message_parts(full_msg)

	# if full_msg.is_multipart():
	# 	# Most messages are multipart (i.e. plain text and html at least)
	# 	for part in full_msg.get_payload():
	# 		if 'text/plain' in part.get_content_type():
	# 			output['plain'] = part.get_payload(decode=True)
	# 		elif 'text/html' in part.get_content_type():
	# 			output['html'] = part.get_payload(decode=True)
	
	# else:
	# 	if 'text/plain' in full_msg.get_content_type():
	# 		output['plain'] = full_msg.get_payload(decode=True)
	# 	elif 'text/html' in full_msg.get_content_type():
	# 		output['html'] = full_msg.get_payload(decode=True)


	return output

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

	# Get all the emails and put them into args
	msgs = Email.objects.all().order_by('id')  # For now just get all emails, later we should filter based on user, date, etc.
	
	# # Now clean up the subject and sender for the messages on this page
	all_emails = []
	for msg in msgs:
		
		sender_data = parse_sender(msg.sender)

		setattr(msg, 'sender', trim_string(sender_data['name'],30))

		new_subject = trim_string(msg.subject,700)
		setattr(msg, 'subject', new_subject)

		all_emails.append(msg)

	# Pagination for the emails
	paginator = Paginator(all_emails, 50)

	page = request.GET.get('page')
	try:
		all_emails = paginator.page(page)
	except PageNotAnInteger:
		all_emails = paginator.page(1)
	except EmptyPage:
		all_emails = paginator.page(paginator.num_pages)

	# Put it into the args dictionary to send to the template
	args['emails'] = all_emails
	
	args['current_page'] = 'classify'
	return render(request, 'classify.html', args)

def extract_view(request):
	args = {}
	args['current_page'] = 'extract'
	return render(request, 'extract.html', args)


def all_email_view(request):
	
	args = {}

	# Get all the emails and put them into args
	msgs = Email.objects.all().order_by('id')  # For now just get all emails, later we should filter based on user, date, etc.
	
	# # Now clean up the subject and sender for the messages on this page
	all_emails = []
	for msg in msgs:
		
		sender_data = parse_sender(msg.sender)

		setattr(msg, 'sender', trim_string(sender_data['name'],30))

		new_subject = trim_string(msg.subject,700)
		setattr(msg, 'subject', new_subject)

		all_emails.append(msg)

	# Pagination for the emails
	paginator = Paginator(all_emails, 50)

	page = request.GET.get('page')
	try:
		all_emails = paginator.page(page)
	except PageNotAnInteger:
		all_emails = paginator.page(1)
	except EmptyPage:
		all_emails = paginator.page(paginator.num_pages)

	# Put it into the args dictionary to send to the template
	args['emails'] = all_emails
	
	args['current_page'] = 'inbox'

	return render(request, 'all_email.html', args)

def email_detail_view(request, email_pk):

	args = {}

	msg = Email.objects.get(pk=email_pk)

	# Get the body
	args['body'] = retrieve_body(msg)
	args['encoded'] = args['body']['html']

	args['email'] = msg

	args['current_page'] = 'email_detail'


	

	return render(request, 'email_detail.html', args)
	# return render_to_response('email_detail.html', args)

def email_set_promotion(request, email_pk):

	# Get the instance of the email object
	instance = Email.objects.get(pk = email_pk)

	instance.set_truth_type('Promotion')
	instance.save()

	a = request.META['HTTP_REFERER']

	return redirect(a)
