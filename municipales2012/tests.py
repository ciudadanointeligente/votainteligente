# -*- coding: utf-8 -*-


from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Comuna, Region, Area, Indice

class RegionModelTestCase(TestCase):
	def test_create_region(self):
		region, created = Region.objects.get_or_create(nombre=u"La región")


	def test_region_unicode(self):
		region = Region.objects.create(nombre=u"Region Metropolitana")

		self.assertEquals(region.__unicode__(), region.nombre)


class ComunaModelTestCase(TestCase):
	def test_create_comuna(self):
		region = Region.objects.create(nombre=u"La región")
		comuna, created = Comuna.objects.get_or_create(nombre=u"La comuna", 
														region=region, 
														slug=u"la-comuna",
														candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		self.assertTrue(created)
		self.assertEquals(comuna.nombre, u"La comuna")
		self.assertEquals(comuna.slug, u"la-comuna")
		self.assertEquals(comuna.region, region)
		self.assertEquals(comuna.candideitorg, u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")

	def test_comuna_unicode(self):
		region = Region.objects.create(nombre=u"La región")
		comuna = Comuna.objects.create(nombre=u"La comuna", region=region, slug=u"la-comuna")

		self.assertEquals(comuna.__unicode__(), comuna.nombre)


class AreaTestCase(TestCase):
	def test_create_area(self):
		area, created = Area.objects.get_or_create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.assertTrue(created)
		self.assertEquals(area.nombre, u'Caracterización')
		self.assertEquals(area.clase_en_carrusel,u"fondoCeleste")

	def test_unicode(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.assertEquals(area.__unicode__(), u"Caracterización")





class IndiceTestCase(TestCase):
	def test_create_indice(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		region = Region.objects.create(nombre=u"La región")
		comuna = Comuna.objects.create(nombre=u"La comuna", 
										region=region, 
										slug=u"la-comuna",
										candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		indice, created = Indice.objects.get_or_create(
			comuna =comuna,
			area = area,
			nombre = u"Pobreza",
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


		self.assertTrue(created)
		self.assertEquals(indice.comuna, comuna)
		self.assertEquals(indice.area, area)
		self.assertEquals(indice.nombre, u"Pobreza")
		self.assertEquals(indice.encabezado, u"encabezado")
		self.assertEquals(indice.numero_1, u"7%")
		self.assertEquals(indice.texto_1, u"de los habitantes de la comuna son pobres")
		self.assertEquals(indice.numero_2, u"n2")
		self.assertEquals(indice.texto_2, u"t2")
		self.assertEquals(indice.texto_pie_pagina_1, u"En el Ranking nacional de pobreza, la comuna está en el lugar")
		self.assertEquals(indice.numero_pie_pagina_1, u"1")
		self.assertEquals(indice.texto_pie_pagina_2,u"tpp2")
		self.assertEquals(indice.numero_pie_pagina_2,u"2")
		self.assertEquals(indice.texto_pie_pagina_3, u"tpp3")
		self.assertEquals(indice.numero_pie_pagina_3, u"3")

	def test_unicode(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste", segunda_clase=u"colorCeleste")
		region = Region.objects.create(nombre=u"La región")
		comuna = Comuna.objects.create(nombre=u"La comuna", 
										region=region, 
										slug=u"la-comuna",
										candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		indice = Indice.objects.create(	
			comuna =comuna,
			area = area,
			nombre = u"Ingreso por persona",
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la comuna",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la comuna está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = False)

		self.assertEquals(indice.__unicode__(), u"Ingreso por persona - La comuna")

	
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
	def setUp(self):
		self.area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.region = Region.objects.create(nombre=u"La región")
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1", region=self.region)
		self.comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2", region=self.region)
		self.indice1 = Indice.objects.create(
			comuna =self.comuna1,
			area = self.area,
			nombre = u"Pobreza",
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

		self.indice3 = Indice.objects.create(	
			comuna =self.comuna2,
			area = self.area,
			nombre = u"Ingreso por persona",
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la comuna",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la comuna está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = True)

	def test_get_comuna_view(self):
		url = reverse('comuna-overview', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'municipales2012/comuna_detail.html')
		self.assertTrue('comuna' in response.context)
		self.assertEquals(response.context['comuna'], self.comuna1)


	def test_get_indices_comunales(self):
		url = reverse('comuna-overview', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)

		self.assertTrue('indices' in response.context)
		self.assertEquals(response.context['indices'].count(), 1)
		self.assertEquals(response.context['indices'][0], self.indice1)

	def test_muestra_solo_los_indices_que_estan_en_el_carrusel(self):
		indice2 = Indice.objects.create(	
			comuna =self.comuna1,
			area = self.area,
			nombre = u"Ingreso por persona",
			encabezado = u"encabezado",
			numero_1 = u"$418.891",
			texto_1 = u"es el promedio de ingreso por persona en la comuna",
			numero_2 = u"n2",
			texto_2 = u"t2",
			texto_pie_pagina_1 = u"En el Ranking nacional de ingreso por persona, la comuna está en el lugar",
			numero_pie_pagina_1 = u"8",
			texto_pie_pagina_2 = u"El promedio nacional de ingreso por persona es",
			numero_pie_pagina_2 = u"X",
			texto_pie_pagina_3 = u"tpp3",
			numero_pie_pagina_3 = u"3",
			en_carrusel = False)
		url = reverse('comuna-overview', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)


		self.assertEquals(response.context['indices'].count(), 1)
		self.assertEquals(response.context['indices'][0], self.indice1) # y no el indice2 que dice False en su campo en_carrusel


