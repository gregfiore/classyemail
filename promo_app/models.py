from django.db import models
from django.utils import timezone

class Email(models.Model):
	sender = models.CharField(max_length=100)
	recipient = models.CharField(max_length=100)
	date = models.DateTimeField()
	subject = models.CharField(max_length=200)
	body_plain = models.CharField(max_length=1000)
	body_html = models.CharField(max_length=1000)
	auto_type = models.IntegerField(null=True)
	truth_type = models.IntegerField(null=True)
