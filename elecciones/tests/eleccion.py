# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from elecciones.models import Eleccion, Area, Indice, Dato, Candidato, Pregunta, Respuesta, Contacto, Colectivo, preguntas_por_partido
from elecciones.management.commands.elecciones_importer import *
from elecciones.management.commands.contactos_importer import *
from elecciones.management.commands.candidatos_importer import *
from mailer.models import Message
from django.test.client import Client
from django.utils.unittest import skip
from django.template import Template, Context
from urllib2 import quote

class EleccionModelTestCase(TestCase):
	def setUp(self):
	    super(EleccionModelTestCase, self).setUp()
	    self.eleccion, created = Eleccion.objects.get_or_create (nombre=u"La eleccion",
	    													slug=u"la-eleccion",
	    													candideitorg_api_key=u"api-key",
	    													main_embedded=u"http://www.candideit.org/usuario-candideitorg/la-eleccion/embeded",
	    													messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
	    													mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
	    													featured=True,
	    													searchable=True
	    													)

	def test_create_eleccion(self):
		self.assertTrue(self.eleccion)
		self.assertEquals(self.eleccion.nombre, u"La eleccion")
		self.assertEquals(self.eleccion.slug, u"la-eleccion")
		self.assertEquals(self.eleccion.main_embedded, u"http://www.candideit.org/usuario-candideitorg/la-eleccion/embeded")
		self.assertEquals(self.eleccion.messaging_extra_app_url, u"http://napistejim.cz/address=nachod")
		self.assertEquals(self.eleccion.mapping_extra_app_url, u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.assertTrue(self.eleccion.featured)

	def test_eleccion_unicode(self):
		self.assertEquals(self.eleccion.__unicode__(), self.eleccion.nombre)

	def test_parsing_user_slug_from_candideitorg(self):
		self.assertEqual(self.eleccion.candideitorg_username(), u"usuario-candideitorg")
		self.assertEqual(self.eleccion.candideitorg_election_slug(), u"la-eleccion")
		self.assertEqual(self.eleccion.candideitorg_api_key, u"api-key")
