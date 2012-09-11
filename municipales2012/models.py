from django.db import models

# Create your models here.


class Comuna(models.Model):
	nombre =  models.CharField(max_length=255)
	slug =  models.CharField(max_length=255)
	candideitorg = models.CharField(max_length=512)

	def __unicode__(self):
		return self.nombre


class Area(models.Model):
	nombre = models.CharField(max_length=255)
	clase_en_carrusel = models.CharField(max_length=255)
	segunda_clase = models.CharField(max_length=255)
	link_detalle = models.CharField(max_length=255)

	def __unicode__(self):
		return self.nombre


class Dato(models.Model):
	nombre = models.CharField(max_length=255)
	imagen = models.CharField(max_length=255)

	def __unicode__(self):
		return self.nombre

class Indice(models.Model):
	comuna = models.ForeignKey(Comuna)
	area = models.ForeignKey(Area)
	dato = models.ForeignKey(Dato)
	encabezado = models.CharField(max_length=255)
	numero_1 = models.CharField(max_length=255)
	texto_1 = models.CharField(max_length=255)
	numero_2 = models.CharField(max_length=255)
	texto_2 = models.CharField(max_length=255)
	texto_pie_pagina_1 = models.CharField(max_length=255)
	numero_pie_pagina_1 = models.CharField(max_length=255)
	texto_pie_pagina_2 = models.CharField(max_length=255)
	numero_pie_pagina_2 = models.CharField(max_length=255)
	texto_pie_pagina_3 = models.CharField(max_length=255)
	numero_pie_pagina_3 = models.CharField(max_length=255)
	en_carrusel = models.BooleanField(default=False)


	def __unicode__(self):
		return self.dato.nombre+' - '+self.comuna.nombre