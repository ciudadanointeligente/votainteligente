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

from municipales2012.views import Ranking


class RankingTestCase(TestCase):

	def setUp(self):
		self.comuna1, created = Comuna.objects.get_or_create(nombre="comuna1", 
			slug="la-comuna1",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.comuna2, created = Comuna.objects.get_or_create(nombre="comuna2", 
			slug="la-comuna2",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.comuna3, created = Comuna.objects.get_or_create(nombre="comuna3", 
			slug="la-comuna3",
			main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
			messaging_extra_app_url="http://napistejim.cz/address=nachod",
			mapping_extra_app_url="http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.colectivo1 = Colectivo.objects.create(sigla='C1', nombre = 'Colectivo 1')
		self.colectivo2 = Colectivo.objects.create(sigla='C2', nombre = 'Colectivo 2')
		self.data_candidato = [\
		{'nombre': 'candidato1', 'mail': 'candidato1@test.com', 'mail2' : 'candidato1@test2.com', 'mail3' : 'candidato1@test3.com', 'comuna': self.comuna1, 'partido':self.colectivo1, 'web': 'web1'},\
		{'nombre': 'candidato2', 'mail': 'candidato2@test.com', 'comuna': self.comuna2, 'partido': self.colectivo1},\
		{'nombre': 'candidato3', 'mail': 'candidato3@test.com', 'comuna': self.comuna3, 'partido':self.colectivo2}]
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		

		self.candidato1 = Candidato.objects.create(nombre=u"candidato1", comuna = self.comuna1, colectivo = self.data_candidato[0]['partido'], web = self.data_candidato[0]['web'])
		self.candidato2 = Candidato.objects.create(nombre=u"candidato2", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		self.candidato3 = Candidato.objects.create(nombre=u"candidato3", comuna = self.comuna1, colectivo = self.data_candidato[2]['partido'])
		self.candidato4 = Candidato.objects.create(nombre=u"candidato4", comuna = self.comuna1, colectivo = self.data_candidato[2]['partido'])
		
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])
		Candidato.objects.create(nombre=u"candidato_molesto", comuna = self.comuna1, colectivo = self.data_candidato[1]['partido'])

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')
		self.respuesta1 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato1)
		self.respuesta2 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato2)
		self.respuesta3 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato3)
		self.respuesta1_c4 = Respuesta.objects.create(pregunta=self.pregunta1, candidato=self.candidato4)

		self.pregunta2 = Pregunta.objects.create(
											remitente='remitente2', 
											texto_pregunta='texto_pregunta2')
		self.respuesta4 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato1)
		self.respuesta5 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato2)
		self.respuesta6 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato3)
		self.respuesta2_c4 = Respuesta.objects.create(pregunta=self.pregunta2, candidato=self.candidato4)

		self.pregunta3 = Pregunta.objects.create(
											remitente='remitente3', 
											texto_pregunta='texto_pregunta3')

		self.respuesta3_1 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato1)
		self.respuesta3_2 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato2)
		self.respuesta3_3 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato3)
		self.respuesta3_4 = Respuesta.objects.create(pregunta=self.pregunta3, candidato=self.candidato4)



		#el candidato1 respondiendo

		self.respuesta1.texto_respuesta = u"Yo opino que guau guau"
		self.respuesta1.save()
		self.respuesta4.texto_respuesta = u"GUAAAAAAAAUUUUUUUwra"
		self.respuesta4.save()
		self.respuesta3_1.texto_respuesta = u"yo soy un campeón"
		self.respuesta3_1.save()
		#el candidato2 respondiendo
		self.respuesta5.texto_respuesta = u"miau miau"
		self.respuesta3_2.texto_respuesta = u"asdasdxcvxcvxcvxcv"
		self.respuesta3_2.save()
		self.respuesta5.save()
		#el candidato 4 ha respondido una pregunta
		self.respuesta3_4.texto_respuesta = u"asdasd"
		self.respuesta3_4.save()
		#el candidato3 es un pajero y no responde niuna cuestion


	def test_obtiene_ranking_candidatos_que_han_respondido_menos(self):

		view = Ranking()
		los_mas_malos = view.malos()

		self.assertEquals(len(los_mas_malos), 4)
		self.assertEquals(los_mas_malos[0]["candidato"], self.candidato3)
		self.assertEquals(los_mas_malos[0]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[0]["preguntas_respondidas"], 0)
		self.assertEquals(los_mas_malos[0]["preguntas_no_respondidas"], 3)

		self.assertEquals(los_mas_malos[1]["candidato"], self.candidato4)
		self.assertEquals(los_mas_malos[1]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[1]["preguntas_respondidas"], 1)
		self.assertEquals(los_mas_malos[1]["preguntas_no_respondidas"], 2)


		self.assertEquals(los_mas_malos[2]["candidato"], self.candidato2)
		self.assertEquals(los_mas_malos[2]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[2]["preguntas_respondidas"], 2)
		self.assertEquals(los_mas_malos[2]["preguntas_no_respondidas"], 1)

		self.assertEquals(los_mas_malos[3]["candidato"], self.candidato1)
		self.assertEquals(los_mas_malos[3]["pregunta_count"], 3)
		self.assertEquals(los_mas_malos[3]["preguntas_respondidas"], 3)
		self.assertEquals(los_mas_malos[3]["preguntas_no_respondidas"], 0)


	def test_get_ranking_html(self):
		url = reverse('ranking')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTrue('malos' in response.context)
		self.assertTemplateUsed(response, 'municipales2012/ranking.html')

		self.assertEquals(len(response.context["malos"]), 4)
		self.assertEquals(response.context["malos"][0]["candidato"], self.candidato3)
		self.assertEquals(response.context["malos"][1]["candidato"], self.candidato4)
		self.assertEquals(response.context["malos"][2]["candidato"], self.candidato2)
		self.assertEquals(response.context["malos"][3]["candidato"], self.candidato1)

		self.assertEquals(len(response.context["buenos"]), 4)
		self.assertEquals(response.context["buenos"][0]["candidato"], self.candidato1)
		self.assertEquals(response.context["buenos"][1]["candidato"], self.candidato2)
		self.assertEquals(response.context["buenos"][2]["candidato"], self.candidato4)
		self.assertEquals(response.context["buenos"][3]["candidato"], self.candidato3)



	def test_get_ranking_de_los_buenos(self):
		view = Ranking()
		los_mas_buenos = view.buenos()

		self.assertEquals(len(los_mas_buenos), 4)
		self.assertEquals(los_mas_buenos[0]["candidato"], self.candidato1)
		self.assertEquals(los_mas_buenos[0]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[0]["preguntas_respondidas"], 3)
		self.assertEquals(los_mas_buenos[0]["preguntas_no_respondidas"], 0)

		self.assertEquals(los_mas_buenos[1]["candidato"], self.candidato2)
		self.assertEquals(los_mas_buenos[1]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[1]["preguntas_respondidas"], 2)
		self.assertEquals(los_mas_buenos[1]["preguntas_no_respondidas"], 1)


		self.assertEquals(los_mas_buenos[2]["candidato"], self.candidato4)
		self.assertEquals(los_mas_buenos[2]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[2]["preguntas_respondidas"], 1)
		self.assertEquals(los_mas_buenos[2]["preguntas_no_respondidas"], 2)

		self.assertEquals(los_mas_buenos[3]["candidato"], self.candidato3)
		self.assertEquals(los_mas_buenos[3]["pregunta_count"], 3)
		self.assertEquals(los_mas_buenos[3]["preguntas_respondidas"], 0)
		self.assertEquals(los_mas_buenos[3]["preguntas_no_respondidas"], 3)


		
