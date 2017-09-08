from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
	avatar = models.ImageField(null=True, blank=True)

	def __unicode__(self):
		return self.first_name
