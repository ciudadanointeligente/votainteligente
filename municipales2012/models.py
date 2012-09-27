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
	link_detalle = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.nombre


class Dato(models.Model):
	nombre = models.CharField(max_length=255)
	imagen = models.CharField(max_length=255, blank=True, null=True)

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

class Candidato(models.Model):
	nombre = models.CharField(max_length=255)
	mail = models.CharField(max_length=255)
	comuna = models.ForeignKey(Comuna)
	partido = models.CharField(max_length=255)
	web = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.nombre

class ManagerPregunta(models.Manager):
	def crear_pregunta(self,texto_pregunta,remitente,destinatarios):
		pregunta = self.create(remitente=remitente,texto_pregunta=texto_pregunta)
		for destinatario in destinatarios:
			Respuesta.objects.create(candidato=destinatario, pregunta=pregunta, texto_respuesta='Sin Respuesta')
		return pregunta
	

class Pregunta(models.Model):
	"""docstring for Pregunta"""
	candidato = models.ManyToManyField('Candidato', through='Respuesta')
	remitente = models.CharField(max_length=255)
	texto_pregunta = models.TextField()
	
	objects = ManagerPregunta()
	
	def __unicode__(self):
		return self.texto_pregunta
		

class Respuesta(models.Model):
	"""docstring for Respuesta"""
	pregunta = models.ForeignKey(Pregunta)
	candidato = models.ForeignKey(Candidato)
	texto_respuesta = models.TextField()

	def __unicode__(self):
		return self.texto_respuesta


		
		
