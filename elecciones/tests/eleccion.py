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
	def test_create_eleccion(self):
		eleccion, created = Eleccion.objects.get_or_create(nombre=u"La eleccion", 
														slug=u"la-eleccion",
														candideitorg_api_key=u"api-key",
														main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
														messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
														mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
														featured=True)
		self.assertTrue(created)
		self.assertEquals(eleccion.nombre, u"La eleccion")
		self.assertEquals(eleccion.slug, u"la-eleccion")
		self.assertEquals(eleccion.main_embedded, u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		self.assertEquals(eleccion.messaging_extra_app_url, u"http://napistejim.cz/address=nachod")
		self.assertEquals(eleccion.mapping_extra_app_url, u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.assertTrue(eleccion.featured)

	def test_eleccion_unicode(self):
		eleccion = Eleccion.objects.create(nombre=u"La eleccion", slug=u"la-eleccion")

		self.assertEquals(eleccion.__unicode__(), eleccion.nombre)

	def test_parsing_user_slug_from_candideitorg(self):
		eleccion, created = Eleccion.objects.get_or_create (nombre=u"La eleccion",
															slug=u"la-eleccion",
															candideitorg_api_key=u"api-key",
															main_embedded=u"http://candideit.org/usuario-candideitorg/la-eleccion/embeded",
															messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
															mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
															featured=False,
															searchable=True
															)
		self.assertEqual(eleccion.candideitorg_username(), u"usuario-candideitorg")
		self.assertEqual(eleccion.candideitorg_election_slug(), u"la-eleccion")
		self.assertEqual(eleccion.candideitorg_api_key, u"api-key")
