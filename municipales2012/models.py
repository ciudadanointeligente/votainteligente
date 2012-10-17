# -*- coding: utf-8 -*-
from django.core.validators import MaxLengthValidator
from django.db import models
from mailer import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models import Count
# from django.core.mail import send_mail
# Create your models here.


class Comuna(models.Model):
	nombre =  models.CharField(max_length=255)
	slug =  models.CharField(max_length=255)
	main_embedded = models.CharField(max_length=512, blank=True, null=True)
	messaging_extra_app_url = models.CharField(max_length=512, blank=True, null=True)
	mapping_extra_app_url = models.CharField(max_length=512, blank=True, null=True)
	
	def __unicode__(self):
		return self.nombre
	def preguntas(self):
		candidatos_comuna = Candidato.objects.filter(comuna=self)
		preguntas_candidatos_comuna = Pregunta.objects.filter(candidato__in=candidatos_comuna).distinct()
		return preguntas_candidatos_comuna
	def numero_preguntas(self):
		preg = self.preguntas()
		return preg.count()
	def numero_respuestas(self):
		resp = Respuesta.objects.filter(pregunta__in=self.preguntas()).exclude(texto_respuesta='Sin Respuesta').distinct()
		return resp.count()



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

class SinDatos(models.Manager):
	def get_query_set(self):
		#Annotate hace que a cada candidato tenga un campo extra
		#llamado contacto_count que es la cantidad de contactos
		#entonces puedes decirle a los objetos resultado de este queryset
		#candidato.contacto_count
		#y debería ser 0 el resultado por que filtramos por eso
		#los Q objects permiten hacer consultas complejas de sql
		#por ejemplo hacer varios ors
		return super(SinDatos, self).get_query_set().annotate(contacto_count=Count('contacto'))\
												.filter(\
													Q(twitter__isnull=True) \
													| Q(twitter__exact='') | \
													Q(contacto_count=0))

class Colectivo(models.Model):
	sigla = models.CharField(max_length=255)
	nombre = models.CharField(max_length=255, blank=True, null=True)
	def __unicode__(self):
		return self.sigla

class Candidato(models.Model):
	nombre = models.CharField(max_length=255)
	#mail = models.CharField(max_length=255)
	comuna = models.ForeignKey(Comuna)
	colectivo = models.ForeignKey(Colectivo, null=True)
	partido = models.CharField(max_length=255)
	web = models.CharField(max_length=255, blank=True, null=True)
	twitter = models.CharField(max_length=255, null=True, blank=True)

	#managers
	objects = models.Manager()
	sin_datos = SinDatos()

	def __unicode__(self):
		return self.nombre

	def _estrellitas(self):
		if self.contacto_set.count() == 0:
			return 3
		if self.contacto_set.filter(tipo=1).count() > 0:
			return 1
		if self.contacto_set.filter(tipo=2).count() > 0:
			return 2
		
		return None

	estrellitas = property(_estrellitas)

	def numero_preguntas(self):
		return self.pregunta.count()

	def respuestas(self):
		preg = Pregunta.objects.filter(candidato=self).distinct()
		resp = Respuesta.objects.filter(pregunta__in=preg).filter(candidato=self).exclude(texto_respuesta='Sin Respuesta').distinct()
		return resp


	def _preguntas_respondidas(self):
		preguntas = self.pregunta.exclude(respuesta__texto_respuesta="Sin Respuesta")
		return preguntas


	preguntas_respondidas = property(_preguntas_respondidas)

	def numero_respuestas(self):
		resp = self.respuestas()
		return resp.count()

	def _has_twitter(self):
		if self.twitter:
			return True
		return False

	has_twitter = property(_has_twitter)

	def _has_contacto(self):
		if self.contacto_set.count() > 0:
			return True
		return False

	has_contacto = property(_has_contacto)


def preguntas_por_partido(self):
	pass
	# print Partido.objects.aggregate(nro_preguntas=Sum('candidatos__numero_preguntas'))






		
class Contacto(models.Model):
	PERSONAL = 1
	PARTIDO = 2
	#Se puede agregar Twitter, FB, etc.
	OTRO = 9
	TIPOS_DE_CONTACTO = (
		(PERSONAL, 'personal'),
		(PARTIDO, 'partido'),
		(OTRO, 'otro'),
	)
	tipo = models.IntegerField(choices=TIPOS_DE_CONTACTO, default=PERSONAL)
	valor = models.CharField(max_length=255)
	candidato = models.ForeignKey(Candidato)

	def __unicode__(self):
		return self.valor

class ManagerPregunta(models.Manager):
	def create(self, **kwargs):
		#Crear pregunta
		destinatarios_pk = kwargs['candidato']
		del kwargs['candidato']
		pregunta = super(ManagerPregunta, self).create(**kwargs)
		pregunta.save()
		#Asociar respuestas
		for destinatario_pk in destinatarios_pk:
			destinatario = Candidato.objects.get(id = destinatario_pk)
			Respuesta.objects.create(candidato=destinatario, pregunta=pregunta)
		return pregunta
	

class Pregunta(models.Model):
	"""docstring for Pregunta"""
	candidato = models.ManyToManyField('Candidato', through='Respuesta', related_name="pregunta")
	remitente = models.CharField(max_length=255)
	texto_pregunta = models.TextField(validators=[MaxLengthValidator(4095)])
	aprobada = models.BooleanField(default=False)
	procesada = models.BooleanField(default=False)
	
	#objects = ManagerPregunta()
	
	def __unicode__(self):
		return self.texto_pregunta

	def enviar(self):
		subject= 'Un ciudadano está interesado en más información sobre tu candidatura [ID=#' + str(self.id) + ']'
		candidatos = Candidato.objects.filter(pregunta=self)
		for candidato in candidatos:
			texto_introduccion = u'Estimado(a) ' + candidato.nombre + ',\reste mensaje ha sido enviado desde votainteligente.cl por un ciudadano con el deseo de informarse sobre su candidatura:'
			texto_cierre = u'\r\r--\r*para responder a esta pregunta responda este mismo correo sin cambiar el asunto/subject. Gracias.\rLa respuesta quedará publicada en http://votainteligente.cl'
			mensaje = texto_introduccion + u'\r\rYo, ' + self.remitente + ' quiero saber: \r\r' + self.texto_pregunta + texto_cierre
			destinaciones = Contacto.objects.filter(candidato=candidato)
			for destinacion in destinaciones:
				send_mail(subject, mensaje, 'municipales2012@votainteligente.cl',[destinacion.valor])

			

		

class Respuesta(models.Model):
	"""docstring for Respuesta"""
	pregunta = models.ForeignKey(Pregunta)
	candidato = models.ForeignKey(Candidato)
	texto_respuesta = models.TextField(default = 'Sin Respuesta')

	def __unicode__(self):
		return self.texto_respuesta

	def get_absolute_url(self):
		url = reverse('comuna-preguntales', kwargs={'slug':self.candidato.comuna.slug})
		return url+"#"+str(self.id)

	def is_answered(self):
		if self.texto_respuesta.strip() == u"Sin Respuesta":
			return False
		return True


		
		
