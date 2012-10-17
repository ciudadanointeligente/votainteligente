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


class HomeTestCase(TestCase):
	def test_get_the_home_page(self):
		url = reverse('home')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	
	def test_trae_los_nombres_de_las_comunas_y_las_regiones(self):
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")
		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertTrue(comuna1 in response.context["comunas"])
		self.assertTrue(comuna2 in response.context["comunas"])

	def test_last_questions(self):

		comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre = 'Colectivo 1')
		colectivo2 = Colectivo.objects.create(sigla='C2', nombre = 'Colectivo 2')
		data_candidato = [\
		{'nombre': 'candidato1', 'mail': 'candidato1@test.com', 'mail2' : 'candidato1@test2.com', 'mail3' : 'candidato1@test3.com', 'comuna': comuna1, 'partido':colectivo1, 'web': 'web1'},\
		{'nombre': 'candidato2', 'mail': 'candidato2@test.com', 'comuna': comuna2, 'partido': colectivo1},\
		{'nombre': 'candidato3', 'mail': 'candidato3@test.com', 'comuna': comuna2, 'partido':colectivo2}]
		candidato1 = Candidato.objects.create(nombre=data_candidato[0]['nombre'], comuna = comuna1, colectivo = data_candidato[0]['partido'], web = data_candidato[0]['web'])
		candidato2 = Candidato.objects.create(nombre=data_candidato[1]['nombre'], comuna = comuna1, colectivo = data_candidato[1]['partido'])
		#crea muchas preguntas y respuestas
		for i in range(7):
			texto_pregunta='texto pregunta '+ str(i)
			texto_respuesta='texto respuesta '+ str(i)
			remitente='Remitente ' + str(i)
			pregunta = Pregunta.objects.create(texto_pregunta=texto_pregunta, remitente=remitente)
			Respuesta.objects.create(texto_respuesta = texto_pregunta, pregunta=pregunta, candidato=candidato1)

		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertTrue(comuna1 in response.context["comunas"])
		self.assertTrue(comuna2 in response.context["comunas"])
		self.assertEquals(Pregunta.objects.all().count(), 7)
		self.assertEquals(Respuesta.objects.all().count(), 7)
		self.assertEquals(response.context['ultimas_preguntas'].count(),5)
		self.assertEquals(response.context['ultimas_respuestas'].count(),5)
