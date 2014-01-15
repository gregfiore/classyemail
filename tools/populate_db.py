################################################################
################################################################
# Main script for extracting emlx emails and populating the DB #
################################################################
################################################################

# 1.  Locate all emails within the desired directory 
# 2.  Load emails, extract information, write to database

from emlx_wrapper import get_emlx, extract_emlx
from process_email import *
import psycopg2 # Python Postresql module
import string
import random

##################
# Configurations #
##################

verbose = 0 	   # Print diagnostics to screen if flag == 1
max_messages = 25000 #float('inf')  # Maximum number of messages to import (for testing purposes)
write_to_db = 1  # write emails to database

user_email = ['gregfiore@gmail.com', 'greg.fiore@sloan.mit.edu']  # To identify when the user is the direct recipient of the email

###############################################
###############################################
# STEP 1 :									  # 
# Get all the emails in the desired directory #
###############################################
###############################################

# Lowest directory to search for emails
mail_directory = '/Users/gregfiore/Library/Mail/V2/Mailboxes/Test.mbox/AB029299-BC72-4BE2-ADB0-365FBE50FD93/Data'

# Get all the emlx files with full path
emlx_files = get_emlx(mail_directory)

# Print the number of messages found to the screen
n_messages = len(emlx_files)
print 'Found '+str(n_messages)+' EMLX messages.'

#####################
# Utility Functions #
#####################

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
	db_string = """INSERT INTO promo_app_email ("sender", "recipient", "date", "subject", "body_plain", "body_html") VALUES """
	for i in range(write_increment):
		db_string = db_string + " (%s,%s,%s,%s,%s,%s)"
	db_string = db_string + ";"
	return db_string

##############################################
##############################################
# STEP 2: 									 #
# Iterate through each email and extract the #
# pertinent information                      #
##############################################
##############################################

#################
# STEP 2A:      #
# Initilization #
#################

if write_to_db:
	conn = establishConnection()  # Connect to database
	db_string = init_db_string(1) # Get the string to write N rows to database

msg_cnt = 0   # keep track of the number of messages processed


for emlx_file in emlx_files:

	if msg_cnt > max_messages:
		# We have exceeded the maximum number of messages to process, break loop
		break
	else:

		##########################################
		# STEP 2B: 								 #
		# For each message, extract the info     #
		# from the EMLX files 				 	 #
		##########################################

		# Extract the raw data from the email
		email_data = extract_emlx(emlx_file)
		if verbose:
			# If verbose, print out a description of the email
			print 'Message ' + str(msg_cnt) + ':'
			print email_data['date'] + ' - From: ' + email_data['from'] or '' + ', To: ' + email_data['to'] or ''
			print email_data['subject'] or 'No Subject'
			print '-------------------------------------------------------------'

		###################################################
		# STEP 2C: 										  #
		# Preprocess the email by parsing out sender,     #
		# identifying if direct recipient, and separating #
		# subject words  								  #
		###################################################

		# These will serve as inputs to the classifier
		preprocessed_data = preprocess_email(email_data, user_email)
		if verbose:
			print 'Pre-processing...'

		###############################################
		# STEP 2D: 									  #
		# Write to database                           #
		###############################################

		if write_to_db:
			# If the flag is set to write to the database, append the DB insert string with this information
			db_val_list.append(email_data['from'])
			db_val_list.append(email_data['to'])
			db_val_list.append(email_data['date'])
			db_val_list.append(email_data['subject'])
			db_val_list.append(email_data['body']['body_plain'])
			db_val_list.append(email_data['body']['body_html'])

			# It's more efficient to write multiple rows at a time, so we assemble M rows to insert at a time
			db_count +=1 

			print 'Preparing email to write to database.'

			if db_count == write_increment:
				# M rows have been processed, write to the database
				if verbose:
					print 'Writing ' + str(write_increment) + ' rows to the database.'
				cur = conn.cursor()
				print db_string
				print db_val_list
				# Execute and commit DB insert command
				cur.execute(db_string, db_val_list)	# Execute the query
				conn.commit()
				# Reset the counter and the variable list
				db_val_list = []
				db_count = 0




	# Increment the number of messages processed
	msg_cnt += 1


if write_to_db:
	conn.close()	# Close the connection
	print 'Database connection closed.'