# -*- coding: utf-8 -*-

import slumber
import requests
from django.test import TestCase
from elecciones.models import Eleccion, Candidato
from django.utils.unittest import skip

class ApiClientTestCase(TestCase):
	def setUp(self):
	    super(ApiClientTestCase, self).setUp()
	    self.eleccion, created = Eleccion.objects.get_or_create (nombre=u"Metal Gear Solid", 
	    													slug=u"metal-gear-solid",
	    													candideitorg_api_key=u"f50a8858ce665291936755394fffa549aa673f68",
	    													main_embedded=u"http://candideit.org/rezzo/metal-gear-solid/embeded",
	    													messaging_extra_app_url=u"http://www.messaging_extra_app_url.example",
	    													mapping_extra_app_url=u"http://www.mapping_extra_app_url.example",
	    													featured=False,
	    													searchable=True
	    													)
	    self.api_url = 'http://candideit.org/api/v1/'

	def test_connecting_to_candideitorg(self):
		params_url = 'election/?username=' + self.eleccion.candideitorg_username() + '&api_key=' + self.eleccion.candideitorg_api_key

		http_response = requests.get(self.api_url + params_url)
		self.assertEqual(http_response.status_code, 200)

		http_response_invalid = requests.get(self.api_url + params_url + 'invalid_api_key')
		self.assertEqual(http_response_invalid.status_code, 401)

	def test_getting_candidates_per_election(self):
		candidatos = self.eleccion.candidatos_presentes()
		self.assertEqual(candidatos[0]['name'], 'Big Boss')
		self.assertEqual(candidatos[0]['resource_uri'], '/api/v1/candidate/5433/')
		self.assertEqual(candidatos[1]['name'], 'Solid Snake')
		self.assertEqual(candidatos[1]['resource_uri'], '/api/v1/candidate/5434/')

	def test_quantity_of_candidates_per_election(self):
		self.assertEqual(self.eleccion.numero_candidatos_presentes(), 2)

