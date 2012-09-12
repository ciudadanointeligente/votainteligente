# -*- coding: utf-8 -*-


from django.test import TestCase
from django.core.urlresolvers import reverse
from models import Comuna, Area, Indice, Dato
from management.commands.comunas_importer import *


class ComunaModelTestCase(TestCase):
	def test_create_comuna(self):
		comuna, created = Comuna.objects.get_or_create(nombre=u"La comuna", 
														slug=u"la-comuna",
														candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		self.assertTrue(created)
		self.assertEquals(comuna.nombre, u"La comuna")
		self.assertEquals(comuna.slug, u"la-comuna")
		self.assertEquals(comuna.candideitorg, u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")

	def test_comuna_unicode(self):
		comuna = Comuna.objects.create(nombre=u"La comuna", slug=u"la-comuna")

		self.assertEquals(comuna.__unicode__(), comuna.nombre)


class AreaTestCase(TestCase):
	def test_create_area(self):
		area, created = Area.objects.get_or_create(
			nombre=u"Caracterización", 
			clase_en_carrusel=u"fondoCeleste", 
			link_detalle=u"./metodologia.html#Pobreza")

		
		self.assertTrue(created)
		self.assertEquals(area.nombre, u'Caracterización')
		self.assertEquals(area.clase_en_carrusel,u"fondoCeleste")
		self.assertEquals(area.link_detalle, u"./metodologia.html#Pobreza")

	def test_unicode(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.assertEquals(area.__unicode__(), u"Caracterización")


class DatoTestCase(TestCase):
	def test_create_dato(self):
		dato, created = Dato.objects.get_or_create(nombre=u"Pobreza", imagen="chanchito.png")

		self.assertTrue(created)
		self.assertEquals(dato.nombre, u"Pobreza")
		self.assertEquals(dato.imagen, u"chanchito.png")


	def test_unicode(self):
		dato = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")


		self.assertEquals(dato.__unicode__(), u"Pobreza")





class IndiceTestCase(TestCase):
	def test_create_indice(self):
		area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		comuna = Comuna.objects.create(nombre=u"La comuna", 
										slug=u"la-comuna",
										candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		indice, created = Indice.objects.get_or_create(
			comuna =comuna,
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


		self.assertTrue(created)
		self.assertEquals(indice.comuna, comuna)
		self.assertEquals(indice.area, area)
		self.assertEquals(indice.dato, pobreza)
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
		ingreso_por_persona = Dato.objects.create(nombre=u"Ingreso por persona", imagen="chanchito.png")
		comuna = Comuna.objects.create(nombre=u"La comuna", 
										slug=u"la-comuna",
										candideitorg=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		indice = Indice.objects.create(	
			comuna =comuna,
			area = area,
			dato = ingreso_por_persona,
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
		comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")
		url = reverse('home')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertTrue(comuna1 in response.context["comunas"])
		self.assertTrue(comuna2 in response.context["comunas"])


class ComunaViewTestCase(TestCase):
	def setUp(self):
		self.area = Area.objects.create(nombre=u"Caracterización", clase_en_carrusel=u"fondoCeleste")
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		self.comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")
		ingreso_por_persona = Dato.objects.create(nombre=u"Ingreso por persona", imagen="chanchito.png")
		pobreza = Dato.objects.create(nombre=u"Pobreza", imagen="chanchito.png")
		self.indice1 = Indice.objects.create(
			comuna =self.comuna1,
			area = self.area,
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

		self.indice2 = Indice.objects.create(	
			comuna =self.comuna1,
			area = self.area,
			dato = pobreza,
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

		self.indice3 = Indice.objects.create(	
			comuna =self.comuna2,
			area = self.area,
			dato = ingreso_por_persona,
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
			en_carrusel = True
			)
		

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
		
		url = reverse('comuna-overview', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)


		self.assertEquals(response.context['indices'].count(), 1)
		self.assertEquals(response.context['indices'][0], self.indice1) # y no el indice2 que dice False en su campo en_carrusel


	def test_get_todos_los_indices_de_una_comuna(self):
		url = reverse('comuna-index-detail', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertTrue("comuna" in response.context)
		self.assertEquals(response.context["comuna"], self.comuna1)
		self.assertTrue("indices" in response.context)
		self.assertEquals(response.context["indices"].count(), 2)
		self.assertTrue(self.indice1 in response.context['indices'])
		self.assertTrue(self.indice2 in response.context['indices'])
		self.assertTemplateUsed(response, "municipales2012/todos_los_indices.html")
		self.assertTemplateUsed(response, "base.html")



class CsvReaderTestOneLine(TestCase):
    def setUp(self):
        self.csvreader = CsvReader()
        self.line =[u"Algarrobo",u"Caracterización",u"Pobreza",u"encabezado","3,97",
            u"Es el porcentaje de habitantes de la comuna que viven bajo la línea de la pobreza",u"n2",u"t2",
            u"En el ranking nacional de pobreza, la comuna se ubica en el lugar",u"326",u" y eso es malo"]

        self.line1 =[u"Algarrobo",u"Caracterización",u"Desigualdad",u"encabezado","3,97",
            		u"Es el porcentaje de habitantes de la comuna que viven bajo la línea de la pobreza",
            		u"n2",u"t2",u"En el ranking nacional de pobreza, la comuna se ubica en el lugar",u"326",
                    u" y eso es malo"]

        self.line2 =[u"Algarrobo",u"Caracterización",u"Pobreza",u"encabezado2","4",
            u"texto2",u"n2",u"t2",
            u"texto nacional 2",u"426",u" y eso es muy malo"]

    def test_actualiza_indice(self):
        indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line2)

        self.assertEquals(Indice.objects.count(), 1)
        self.assertEquals(indice.comuna.nombre, u"Algarrobo")
        self.assertEquals(indice.area.nombre, u"Caracterización")
        self.assertEquals(indice.dato.nombre, u"Pobreza")
        self.assertEquals(indice.encabezado, u"encabezado2")
        self.assertEquals(indice.numero_1, u"4")
        self.assertEquals(indice.texto_1, u"texto2")
        self.assertEquals(indice.numero_2, u"n2")
        self.assertEquals(indice.texto_2, u"t2")
        self.assertEquals(indice.texto_pie_pagina_1, u"texto nacional 2")
        self.assertEquals(indice.numero_pie_pagina_1, u"426")
        self.assertEquals(indice.texto_pie_pagina_2,u" y eso es muy malo")
    
    def test_detect_indice(self):
    	indice = self.csvreader.detectIndice(self.line)


        self.assertEquals(indice.comuna.nombre, u"Algarrobo")
        self.assertEquals(indice.area.nombre, u"Caracterización")
        self.assertEquals(indice.dato.nombre, u"Pobreza")
        self.assertEquals(indice.encabezado, u"encabezado")
        self.assertEquals(indice.numero_1, u"3,97")
        self.assertEquals(indice.texto_1, u"Es el porcentaje de habitantes de la comuna que viven bajo la línea de la pobreza")
        self.assertEquals(indice.numero_2, u"n2")
        self.assertEquals(indice.texto_2, u"t2")
        self.assertEquals(indice.texto_pie_pagina_1, u"En el ranking nacional de pobreza, la comuna se ubica en el lugar")
        self.assertEquals(indice.numero_pie_pagina_1, u"326")
        self.assertEquals(indice.texto_pie_pagina_2,u" y eso es malo")


    def test_does_not_create_two_indices_for_the_same_comuna_with_the_same_dato(self):
    	indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line)

        self.assertEquals(Indice.objects.count(), 1)

    def test_but_it_does_when_different_dato(self):
        indice = self.csvreader.detectIndice(self.line)
        indice = self.csvreader.detectIndice(self.line1)

        self.assertEquals(Indice.objects.count(), 2)






    def test_detect_comuna_out_of_a_line(self):
        comuna = self.csvreader.detectComuna(self.line)

        self.assertEquals(Comuna.objects.count(), 1)
        self.assertEquals(comuna.nombre, u"Algarrobo")
        self.assertEquals(comuna.slug, u"algarrobo")

    def test_does_not_create_two_comunas(self):
    	comuna = self.csvreader.detectComuna(self.line)
    	comuna = self.csvreader.detectComuna(self.line)


        self.assertEquals(Comuna.objects.count(), 1)

    def test_detect_area(self):
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)
        self.assertEquals(area.nombre, u"Caracterización")


    def test_it_does_not_create_two_areas(self):
        area = self.csvreader.detectArea(self.line)
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)


    def test_detect_dato(self):
        dato = self.csvreader.detectDato(self.line)

        self.assertEquals(dato.nombre, u"Pobreza")

    


