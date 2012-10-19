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


class TemplateTagsTesting(TestCase):
	def setUp(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		self.comuna = Comuna.objects.create(nombre=u"La comuna", 
										slug=u"la-comuna",
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										)
		self.indice = Indice.objects.create(
			comuna =self.comuna,
			area = area,
			dato = pobreza,
			encabezado = u"encabezado",
			numero_1 = u"7%",
			texto_1 = u"de los habitantes de la comuna son pobres",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de pobreza, la comuna está en el lugar",
			numero_pie_pagina_1 = u"1",
			texto_pie_pagina_2 = u"tpp2",
			numero_pie_pagina_2 = u"2",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = True
			)
		self.candidato = Candidato.objects.create(comuna=self.comuna,\
															 nombre=u"el candidato",\
															 partido=u"API",\
															 web=u"http://votainteligente.cl",\
															 twitter=u"candidato")

	def test_no_responden_diles_algo(self):
		expected_html = '<a href="https://twitter.com/intent/tweet" data-text="1 preguntas de ciudadanos no han sido respondidas por @candidato, revisalas en http://www.votainteligente.cl/la-comuna/preguntales" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @candidato</a>'
		template = Template("{% load twitter_tags %}{{ malo|no_responde }}")
		context = Context({"malo": {'candidato':self.candidato,'preguntas_no_respondidas':1} })


		self.assertEqual(template.render(context), expected_html)



	def test_si_responden_dales_las_gracias(self):
		expected_html = '<a href="https://twitter.com/intent/tweet" data-text="Gracias @candidato por responder a los ciudadanos en http://www.votainteligente.cl/la-comuna/preguntales" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @candidato</a>'
		template = Template("{% load twitter_tags %}{{ bueno|si_responde }}")
		context = Context({"bueno": {'candidato':self.candidato,'preguntas_respondidas':1} })


		self.assertEqual(template.render(context), expected_html)


	def test_trae_todas_las_comunas(self):
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", 
									slug=u"la-comuna1",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"")
		comuna1 = Comuna.objects.create(nombre=u"La comuna2", 
									slug=u"la-comuna2",
									main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
									messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
									mapping_extra_app_url=u"")

		expected_html = '{label:"La comuna",value:"la-comuna"},{label:"La comuna1",value:"la-comuna1"},{label:"La comuna2",value:"la-comuna2"}'
		template = Template("{% load comunas %}{% comunas_search %}")

		context = Context({})

		self.assertEqual(template.render(context), expected_html)





