from django.db import models

# Create your models here.


class Comuna(models.Model):
	nombre =  models.CharField(max_length=255)
	slug =  models.CharField(max_length=255)
	main_embedded = models.CharField(max_length=512, blank=True, null=True)
	messaging_extra_app_url = models.CharField(max_length=512, blank=True, null=True)
	mapping_extra_app_url = models.CharField(max_length=512, blank=True, null=True)
	
	def __unicode__(self):
		return self.nombre


class Area(models.Model):
	nombre = models.CharField(max_length=255)
	clase_en_carrusel = models.CharField(max_length=255, blank=True, null=True)
	segunda_clase = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.nombre


class Dato(models.Model):
	nombre = models.CharField(max_length=255)
	imagen = models.CharField(max_length=255, blank=True, null=True)
	link_metodologia = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

class Indice(models.Model):
	comuna = models.ForeignKey(Comuna)
	area = models.ForeignKey(Area)
	dato = models.ForeignKey(Dato)
	encabezado = models.CharField(max_length=255, blank=True, null=True)
	numero_1 = models.CharField(max_length=255, blank=True, null=True)
	texto_1 = models.CharField(max_length=255, blank=True, null=True)
	numero_2 = models.CharField(max_length=255, blank=True, null=True)
	texto_2 = models.CharField(max_length=255, blank=True, null=True)
	texto_pie_pagina_1 = models.CharField(max_length=255, blank=True, null=True)
	numero_pie_pagina_1 = models.CharField(max_length=255, blank=True, null=True)
	texto_pie_pagina_2 = models.CharField(max_length=255, blank=True, null=True)
	numero_pie_pagina_2 = models.CharField(max_length=255, blank=True, null=True)
	texto_pie_pagina_3 = models.CharField(max_length=255, blank=True, null=True)
	numero_pie_pagina_3 = models.CharField(max_length=255, blank=True, null=True)
	en_carrusel = models.BooleanField(default=False)


	def __unicode__(self):
		return self.dato.nombre+' - '+self.comuna.nombre