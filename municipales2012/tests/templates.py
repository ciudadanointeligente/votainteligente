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

class TemplatesViewsTestCase(TestCase):
	def setUp(self):
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		self.comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")


	def test_get_metodologia(self):
		url = reverse('metodologia')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Metodología")
		self.assertTemplateUsed(response, 'municipales2012/metodologia.html')

	def test_get_quienes_somos(self):
		url = reverse('somos')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'municipales2012/quienesSomos.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Quienes somos")

	def test_get_reporta(self):
		url = reverse('reporta')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'municipales2012/reporta.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Fiscaliza")


	def test_get_que_puedo_hacer(self):
		url = reverse('que_puedo_hacer')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'municipales2012/que_puedo_hacer.html')
		self.assertEquals(response.status_code, 200)
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'],u"¿Qué puedo hacer?")
