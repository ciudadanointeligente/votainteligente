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
from django.template import Template, Context, RequestContext
from urllib2 import quote

class MolestaAUnCandidato(TestCase):
	def setUp(self):
		colectivo1 = Colectivo.objects.create(sigla='C1', nombre='Colectivo 1')
		self.eleccion1 = Eleccion.objects.create(nombre=u"La eleccion1", slug=u"la-eleccion1")
		self.candidato_con_twitter = Candidato.objects.create(eleccion=self.eleccion1,\
												 nombre=u"el candidato con twitter",\
												 partido=u"API",\
												 web=u"http://unaurl.cl",\
												 twitter=u"candidato",\
												 colectivo=colectivo1)

		self.candidato_sin_twitter = Candidato.objects.create(eleccion=self.eleccion1,\
												 nombre=u"el candidato sin twitter",\
												 partido=u"API",\
												 web=u"http://votainteURLligente.cl",\
												 colectivo=colectivo1)

		self.pregunta1 = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')

		self.respuesta1 = Respuesta.objects.create(candidato = self.candidato_con_twitter, pregunta = self.pregunta1)
		self.respuesta2 = Respuesta.objects.create(candidato = self.candidato_sin_twitter, pregunta = self.pregunta1)
	
	def test_molesta_a_un_candidato_sin_twitter_por_su_respuesta_via_twitter(self):
		template = Template("{% load twitter_tags %}{{ respuesta|twittrespuesta }}")
		
		context = Context({"respuesta": self.respuesta2 })
		url_respuesta = self.respuesta2.get_absolute_url()
		expected_html = u""

		self.assertEqual(template.render(context), expected_html)
	@skip('No tenemos host domain en local')
	def test_molesta_a_un_candidato_con_twitter_por_su_respuesta_via_twitter(self):
		template = Template("{% load twitter_tags %}{{ respuesta|twittrespuesta }}")
		context = Context({"respuesta": self.respuesta1 })
		template2 = Template("{{ request.get_host }}")
		
		url_respuesta = template2.render(Context())+self.respuesta1.get_absolute_url()
		expected_html = u'<a href="https://twitter.com/intent/tweet?screen_name='+self.respuesta1.candidato.twitter+u'" data-text="'+url_respuesta+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+self.respuesta1.candidato.twitter+u'</a>'
		
		self.assertEqual(template.render(context), expected_html)


