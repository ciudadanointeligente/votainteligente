from django.db import models

# Create your models here.
class Region(models.Model):
	nombre = models.CharField(max_length=255)


class Comuna(models.Model):
	nombre =  models.CharField(max_length=255)
	region = models.ForeignKey(Region)