from emlx_wrapper import get_emlx, extract_emlx
from process_email import *
import psycopg2 # Python Postresql module
import string
import mailbox
import re
from email.header import decode_header

mail_file = '/Users/gregfiore/Dropbox/Projects/Email/Dashboard/Inbox/November - Jan 14.mbox/mbox'
start_id = 0
write_db = 1
max_messages = 100

#####################
# Utility Functions #
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

def establishConnection():
	# Connect to the database 
	try:
		conn = psycopg2.connect("dbname='classyemail' user='gregfiore' password='letmein' host='/tmp' port='5432'")
		print 'Connected to database...'
		return conn
	except:
		print 'Error accessing database.'
		return None

def init_db_string(write_increment):
	# Initiliaze the string to write N lines to the database
	db_string = """INSERT INTO promo_app_email ("sender", "recipient", "date", "subject", "email_source", "email_key") VALUES """
	for i in range(write_increment):
		db_string = db_string + " (%s,%s,%s,%s,%s,%s)"
	db_string = db_string + ";"
	return db_string

def trim_string(og_string, max_length):
	return (og_string[:(max_length-3)] + '...') if len(og_string) > max_length else og_string

def clean_time(input_time):
	return re.sub(r'\([^)]*\)', '', input_time)

def extract_msg(message):

	data = {'id':'', 'date':'', 'to':'', 'from':'', 'subject':'', 'body':{'plain':'', 'html':''}}

	# Put the appropriate 
	data['id'] = message['message-id']
	data['date'] = message['date']
	data['subject'] = trim_string(message['subject'],200)
	data['from'] = trim_string(message['from'], 100)
	data['to'] = trim_string(message['to'], 100)

	if message.is_multipart():
		# Most messages are multipart (i.e. plain text and html at least)
		for part in message.get_payload():
			if 'text/plain' in part.get_content_type():
				data['body']['plain'] = trim_string(str(part),1000)
			elif 'text/html' in part.get_content_type():
				data['body']['html'] = trim_string(str(part),1000)
	
	else:
		if 'text/plain' in message.get_content_type():
			data['body']['plain'] = trim_string(str(message.get_payload()),1000)
		elif 'text/html' in message.get_content_type():
			data['body']['html'] = trim_string(str(message.get_payload()),1000)

	return data

#################################
# Extract and write to database #
#################################

mbox = mailbox.mbox(mail_file)

# Print the number of messages found to the screen
n_messages = len(mbox)
print 'Found '+str(n_messages)+' messages.'

mail_keys = mbox.keys()

# Connect to the database
if write_db:
	conn = establishConnection()
	db_string = init_db_string(1)

for idx in range(start_id, n_messages-1):
	if idx >= max_messages:
		break

	email_data = extract_msg(mbox[idx])
	print str(idx) + ': Key = ' + str(mail_keys[idx])

	subject, encoding = decode_header(mbox[idx].get('subject'))[0]
	if encoding == 'utf-8':
		sender = parse_sender(mbox[idx].get('from'))
		new_sender = decode_header(sender['name'])[0]
		# print new_sender[0]
		# print sender['address']
		email_data['from'] = email.utils.formataddr((new_sender[0], sender['address']))

		email_data['subject'] = subject.decode(encoding)
		print email_data['from']
		print email_data['subject']

	
	if write_db:
		db_val_list = []
		# If the flag is set to write to the database, append the DB insert string with this information
		db_val_list.append(email_data['from'])
		db_val_list.append(email_data['to'])
		db_val_list.append(clean_time(email_data['date']))
		db_val_list.append(email_data['subject'])
		db_val_list.append(mail_file)
		db_val_list.append(mail_keys[idx])

		# db_val_list.append(email_data['body']['plain'])
		# db_val_list.append(email_data['body']['html'])

		cur = conn.cursor()

		# Execute and commit DB insert command
		cur.execute(db_string, db_val_list)	# Execute the query
		conn.commit()

if write_db:
	conn.close()	# Close the connection
	print 'Database connection closed.'

