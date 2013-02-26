# -*- coding: utf-8 -*-
import slumber
import re
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

class AdminTestCase(TestCase):
	def test_admin_create_eleccion(self):
		eleccion, created = Eleccion.objects.get_or_create (nombre=u"Metal Gear Solid", 
															slug=u"metal-gear-solid",
															candidator_api_key=u"f50a8858ce665291936755394fffa549aa673f68",
															main_embedded=u"http://candideit.org/rezzo/metal-gear-solid/embeded",
															messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
															mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
															featured=False,
															searchable=True
															)
		self.assertTrue(created)
		self.assertEquals(eleccion.nombre, u"Metal Gear Solid")
		self.assertEquals(eleccion.slug, u"metal-gear-solid")
		self.assertEquals(eleccion.candidator_api_key, u"f50a8858ce665291936755394fffa549aa673f68")
		self.assertEquals(eleccion.main_embedded, u"http://candideit.org/rezzo/metal-gear-solid/embeded")
		self.assertEquals(eleccion.messaging_extra_app_url, u"http://napistejim.cz/address=nachod")
		self.assertEquals(eleccion.mapping_extra_app_url, u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.assertFalse(eleccion.featured)
		self.assertTrue(eleccion.searchable)

	def test_candidates_per_election(self):
		eleccion, created = Eleccion.objects.get_or_create (nombre=u"Metal Gear Solid", 
															slug=u"metal-gear-solid",
															candidator_api_key=u"f50a8858ce665291936755394fffa549aa673f68",
															main_embedded=u"http://candideit.org/rezzo/metal-gear-solid/embeded",
															messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
															mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278",
															featured=False,
															searchable=True
															)
		pattern = re.compile('.*candideit\.org\/(.+?)\/([^/]+).*')
		results = pattern.findall(main_embedded)
		
		candidator_username = results[0][0]
		candidator_election_slug = results[0][1]

		candidates_per_election(candidator_election_slug, candidator_username, self.eleccion.api_key)
		#wip
		# TENGO:	uri_eleccion, username, api_key
		# QUIERO:	lista Candidatos con {name, uri}