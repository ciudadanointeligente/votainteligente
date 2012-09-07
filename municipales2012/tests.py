# -*- coding: utf-8 -*-


from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Comuna, Region

class RegionModelTestCase(TestCase):
	def test_create_region(self):
		region, created = Region.objects.get_or_create(nombre=u"La región")


	def test_region_unicode(self):
		region = Region.objects.create(nombre=u"Region Metropolitana")

		self.assertEquals(region.__unicode__(), region.nombre)


class ComunaModelTestCase(TestCase):
	def test_create_comuna(self):
		region = Region.objects.create(nombre=u"La región")
		comuna, created = Comuna.objects.get_or_create(nombre=u"La comuna", region=region, slug=u"la-comuna")
		self.assertTrue(created)
		self.assertEquals(comuna.nombre, u"La comuna")
		self.assertEquals(comuna.slug, u"la-comuna")
		self.assertEquals(comuna.region, region)

	def test_comuna_unicode(self):
		region = Region.objects.create(nombre=u"La región")
		comuna = Comuna.objects.create(nombre=u"La comuna", region=region, slug=u"la-comuna")

		self.assertEquals(comuna.__unicode__(), comuna.nombre)

	
class HomeTestCase(TestCase):
	def test_get_the_home_page(self):
		url = reverse('home')
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	
	def test_trae_los_nombres_de_las_comunas_y_las_regiones(self):
		region = Region.objects.create(nombre=u"La región")
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1", region=region)
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2", region=region)
		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertTrue(comuna1 in response.context["comunas"])
		self.assertTrue(comuna2 in response.context["comunas"])

		self.assertTrue('regiones' in response.context)
		self.assertTrue(region in response.context["regiones"])


class ComunaViewTestCase(TestCase):
	def test_get_comuna_view(self):
		region = Region.objects.create(nombre=u"La región")
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1", region=region)
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2", region=region)
		url = reverse('comuna-overview', kwargs={
			'slug':comuna1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'municipales2012/comuna_detail.html')
		self.assertTrue('comuna' in response.context)
		self.assertEquals(response.context['comuna'], comuna1)


