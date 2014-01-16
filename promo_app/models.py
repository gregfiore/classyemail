from django.db import models
from django.utils import timezone

def get_email_types():
	types = [(0, 'Other'),
				(1, 'Promotion'),
				(2, 'Commerce'),
				(3, 'Travel'),]
	return types

def match_type(current_value, all_values):
	# Match a type enum to a type string (e.g. current_value = 1 returns 'Promotion')
		for value in all_values:
			if current_value == value[0]:
				return value[1]
		return 'Unknown'

def match_type_enum(current_value, all_values):
	# Match a state status to a state enum (e.g. current_value = 'Promotion' returns 1)
		for value in all_values:
			if current_value == value[1]:
				return value[0]
		return 0


class Email(models.Model):
	sender = models.CharField(max_length=100)
	recipient = models.CharField(max_length=100)
	date = models.DateTimeField()
	subject = models.CharField(max_length=200)
	email_source = models.CharField(max_length=200)
	email_key = models.IntegerField()
	auto_type = models.IntegerField(null=True)
	truth_type = models.IntegerField(null=True)
	def get_auto_type(self):
		# To be added:  expired, removed by user, etc.
		return match_type(self.auto_type, get_email_types())
	def get_truth_type(self):
		# To be added:  expired, removed by user, etc.
		return match_type(self.truth_type, get_email_types())

	def set_truth_type(self, new_type):
		type_set = match_type_enum(new_type, get_email_types())
		self.truth_type = type_set
		return
	def set_auto_type(self, new_type):
		type_set = match_type_enum(new_type, get_email_types())
		self.auto_type = type_set
		return