from django.db import models

# Create your models here.
class Region(models.Model):
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return self.nombre


class Comuna(models.Model):
	nombre =  models.CharField(max_length=255)
	region = models.ForeignKey(Region)
	slug =  models.CharField(max_length=255)

	def __unicode__(self):
		return self.nombre