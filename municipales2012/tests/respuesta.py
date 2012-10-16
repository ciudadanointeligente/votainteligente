# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from municipales2012.models import Comuna, Area, Indice, Dato, Candidato, Pregunta, Respuesta, Contacto, Colectivo, preguntas_por_partido
from municipales2012.management.commands.comunas_importer import *
from municipales2012.management.commands.contactos_importer import *
from municipales2012.management.commands.candidatos_importer import *
from mailer.models import Message
from django.test.client import Client
from django.utils.unittest import skip
from django.template import Template, Context
from urllib2 import quote



class RespuestaTestCase(TestCase):
	def setUp(self):
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		self.candidato1 = Candidato.objects.create(comuna=self.comuna1,\
												 nombre=u"el candidato",\
												 partido=u"API",\
												 web=u"http://votainteligente.cl",\
												 twitter=u"candidato",\
												 colectivo=colectivo1)

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')


	def test_create_respuesta(self):
		respuesta, created = Respuesta.objects.get_or_create(candidato = self.candidato1, pregunta = self.pregunta1)

		self.assertTrue(created)
		self.assertEquals(respuesta.candidato, self.candidato1)
		self.assertEquals(respuesta.pregunta, self.pregunta1)
		self.assertEquals(respuesta.texto_respuesta, u"Sin Respuesta")

	def test_get_absolute_url(self):
		respuesta, created = Respuesta.objects.get_or_create(candidato = self.candidato1, pregunta = self.pregunta1)

		url = respuesta.get_absolute_url()
		url_preguntales = reverse('comuna-preguntales', kwargs={'slug':self.comuna1.slug})
		self.assertEquals(url, url_preguntales+"#"+str(respuesta.id))

	def test_is_not_answered(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)

		self.assertFalse(respuesta.is_answered())

	def test_is_answered(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)
		respuesta.texto_respuesta = u"Una respuesta maravillosa del candidato"
		self.assertTrue(respuesta.is_answered())


	def test_is_not_answered_with_spaces(self):
		respuesta = Respuesta.objects.create(candidato = self.candidato1, pregunta = self.pregunta1)
		respuesta.texto_respuesta = u"Sin Respuesta     "#Many spaces at the end

		self.assertFalse(respuesta.is_answered())
