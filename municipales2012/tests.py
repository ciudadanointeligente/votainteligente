# -*- coding: utf-8 -*-


from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Comuna, Region

class RegionModelTestCase(TestCase):
	def test_create_region(self):
		region, created = Region.objects.get_or_create(nombre=u"La región")


class ComunaModelTestCase(TestCase):
	def test_create_comuna(self):
		region = Region.objects.create(nombre=u"La región")
		comuna, created = Comuna.objects.get_or_create(nombre=u"La comuna", region=region)
		self.assertTrue(created)
		self.assertEquals(comuna.nombre, u"La comuna")
		self.assertEquals(comuna.region, region)
	
class HomeTestCase(TestCase):
	def test_get_the_home_page(self):
		url = reverse('home')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	
	def test_trae_los_nombres_de_las_comunas(self):
		region = Region.objects.create(nombre=u"La región")
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", region=region)
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", region=region)

		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertTrue(comuna1 in response.context["comunas"])
		self.assertTrue(comuna2 in response.context["comunas"])