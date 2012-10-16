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


class CandidatoTestCase(TestCase):
	def setUp(self):
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")

	def test_create_candidato(self):
		candidato, created = Candidato.objects.get_or_create(comuna=self.comuna1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteligente.cl",\
															 twitter=u"candidato")

		self.assertTrue(created)
		self.assertEquals(candidato.comuna, self.comuna1)
		self.assertEquals(candidato.nombre, u"el candidato")
		self.assertEquals(candidato.partido, u"API")
		self.assertEquals(candidato.web, u"http://votainteligente.cl")
		self.assertEquals(candidato.twitter, "candidato")


	def test_create_candidato_without_twitter(self):
		candidato, created = Candidato.objects.get_or_create(comuna=self.comuna1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteligente.cl")

		self.assertTrue(created)
		self.assertFalse(candidato.twitter)

	def test_create_candidato_with_empty_twitter(self):
		candidato,created = Candidato.objects.get_or_create(comuna=self.comuna1,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteligente.cl",
															 twitter=u"")
		self.assertTrue(created)
		self.assertFalse(candidato.twitter)