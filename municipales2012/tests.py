# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from models import Comuna, Area, Indice, Dato, Candidato, Pregunta, Respuesta, Contacto
from management.commands.comunas_importer import *
from management.commands.contactos_importer import *
from management.commands.candidatos_importer import *
from django.test.client import Client
from django.utils.unittest import skip


class ComunaModelTestCase(TestCase):
	def test_create_comuna(self):
		comuna, created = Comuna.objects.get_or_create(nombre=u"La comuna", 
														slug=u"la-comuna",
														main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
														messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
														mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
		self.assertTrue(created)
		self.assertEquals(comuna.nombre, u"La comuna")
		self.assertEquals(comuna.slug, u"la-comuna")
		self.assertEquals(comuna.main_embedded, u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded")
		self.assertEquals(comuna.messaging_extra_app_url, u"http://napistejim.cz/address=nachod")
		self.assertEquals(comuna.mapping_extra_app_url, u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")

	def test_comuna_unicode(self):
		comuna = Comuna.objects.create(nombre=u"La comuna", slug=u"la-comuna")

		self.assertEquals(comuna.__unicode__(), comuna.nombre)


class AreaTestCase(TestCase):
	def test_create_area(self):
		area, created = Area.objects.get_or_create(
			nombre=u"Caracterización", 
			clase_en_carrusel=u"fondoCeleste") 

		
		self.assertTrue(created)
		self.assertEquals(area.nombre, u'Caracterización')
		self.assertEquals(area.clase_en_carrusel,u"fondoCeleste")

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
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
										mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
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
										main_embedded=u"http://www.candideit.org/lfalvarez/rayo-x-politico/embeded",
										messaging_extra_app_url=u"http://napistejim.cz/address=nachod",
										mapping_extra_app_url=u"http://vecino.ciudadanointeligente.org/around?latitude=-33.429042;longitude=-70.611278")
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
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertEquals(response.context['comuna'], self.comuna1)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], self.comuna1.nombre)


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
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue("comuna" in response.context)
		self.assertEquals(response.context["comuna"], self.comuna1)
		self.assertTrue("indices" in response.context)
		self.assertEquals(response.context["indices"].count(), 2)
		self.assertTrue(self.indice1 in response.context['indices'])
		self.assertTrue(self.indice2 in response.context['indices'])
		self.assertTemplateUsed(response, "municipales2012/todos_los_indices.html")
		self.assertTemplateUsed(response, "base_sub_menu.html")
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], self.comuna1.nombre + u" índices detallados")


	def atest_get_todos_los_indices_de_una_comuna_como_json(self):
		url = reverse('comuna-index-detail-json', kwargs={
			'slug':self.comuna1.slug
			})
		response = self.client.get(url)

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.content_type, u'application/json')



class CsvReaderTestOneLine(TestCase):
    def setUp(self):
        self.csvreader = CsvReader()
        self.line =["Algarrobo","Caracterización",u"Pobreza",u"encabezado","3,97",
            u"Es el porcentaje de habitantes de la comuna que viven bajo la línea de la pobreza",u"n2",u"t2",
            u"En el ranking nacional de pobreza, la comuna se ubica en el lugar",u"326",u" y eso es malo","247" ,"del ranking nacional", "SI"]

        self.line1 =["Algarrobo","Caracterización",u"Desigualdad",u"encabezado","3,97",
            		u"Es el porcentaje de habitantes de la comuna que viven bajo la línea de la pobreza",
            		u"n2",u"t2",u"En el ranking nacional de pobreza, la comuna se ubica en el lugar",u"326",
                    u" y eso es malo", "247", "del ranking nacional", "SI"]

        self.line2 =["Algarrobo","Caracterización",u"Pobreza",u"encabezado2","4",
            u"texto2",u"n2",u"t2",
            u"texto nacional 2",u"426",u" y eso es muy malo", "247" , "del ranking nacional", "NO"]
        self.line3 =["Algarrobo  ", "Caracterización ", "Pobreza ","encabezado2","4",
            "texto2","n2","t2",
            "texto nacional 2","426"," y eso es muy malo","247","del ranking nacional", "SI"]


    def test_crea_indice_en_carrusel_y_fuera_de_el(self):
    	indice = self.csvreader.detectIndice(self.line1)
    	self.assertTrue(indice.en_carrusel)

        indice = self.csvreader.detectIndice(self.line2)
        self.assertFalse(indice.en_carrusel)


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
        self.assertEquals(indice.texto_pie_pagina_2, u"y eso es muy malo")
        self.assertEquals(indice.texto_pie_pagina_3, u"del ranking nacional")
        self.assertEquals(indice.numero_pie_pagina_2 ,u"247")
        
    
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
        self.assertEquals(indice.texto_pie_pagina_2,u"y eso es malo")


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


    def test_does_not_create_two_comunas_with_spaces(self):
    	comuna = self.csvreader.detectComuna(self.line2)
    	comuna = self.csvreader.detectComuna(self.line3)

        self.assertEquals(Comuna.objects.count(), 1)

    def test_detect_area(self):
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)
        self.assertEquals(area.nombre, u"Caracterización")


    def test_it_does_not_create_two_areas(self):
        area = self.csvreader.detectArea(self.line)
        area = self.csvreader.detectArea(self.line)

        self.assertEquals(Area.objects.count(), 1)

    def test_it_does_not_create_two_areas_even_with_spaces(self):
    	area = self.csvreader.detectArea(self.line2)
    	area = self.csvreader.detectArea(self.line3)

    	self.assertEquals(Area.objects.count(), 1)
    	self.assertEquals(area.nombre, u"Caracterización")


    def test_detect_dato(self):
        dato = self.csvreader.detectDato(self.line)

        self.assertEquals(dato.nombre, u"Pobreza")


    def test_it_does_not_create_twice_the_same_dato(self):
    	dato = self.csvreader.detectDato(self.line2)
    	dato = self.csvreader.detectDato(self.line3)

    	self.assertEquals(Dato.objects.count(), 1)



class TemplatesViewsTestCase(TestCase):
	def setUp(self):
		self.comuna1 = Comuna.objects.create(nombre=u"La comuna1", slug=u"la-comuna1")
		self.comuna2 = Comuna.objects.create(nombre=u"La comuna2", slug=u"la-comuna2")


	def test_get_metodologia(self):
		url = reverse('metodologia')
		response = self.client.get(url)

		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Metodología")
		self.assertTemplateUsed(response, 'municipales2012/metodologia.html')

	def test_get_quienes_somos(self):
		url = reverse('somos')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'municipales2012/quienesSomos.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Quienes somos")

	def test_get_reporta(self):
		url = reverse('reporta')
		response = self.client.get(url)

		self.assertTemplateUsed(response, 'municipales2012/reporta.html')

		self.assertEquals(response.status_code, 200)
		self.assertTrue('comunas' in response.context)
		self.assertEquals(response.context['comunas'].count(), 2)
		self.assertTrue('title' in response.context)
		self.assertEquals(response.context['title'], u"Fiscaliza")


class MessageTestCase(TestCase):

#Load candidate mailing data
#Create mail template
#Create question mail
#Send question mail
#Save question mail in db
#Retrieve question mail from db
#Obtain answer mail
#Save answer mail in db
#Retrieve answer mail from db
#Associate quesion and answer mails
#Obtain questions/answers for a given candidate
#Calculate response stats


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
		self.data_candidato = [{'nombre': 'candidato1', 'mail': 'candidato1@test.com', 'mail2' : 'candidato1@test2.com', 'mail3' : 'candidato1@test3.com', 'comuna': self.comuna1, 'partido':'partido1', 'web': 'web1'},{'nombre': 'candidato2', 'mail': 'candidato2@test.com', 'comuna': self.comuna2, 'partido':'partido2'},{'nombre': 'candidato3', 'mail': 'candidato3@test.com', 'comuna': self.comuna3, 'partido':'partido3'}]
		self.candidato1 = Candidato.objects.create(nombre=self.data_candidato[0]['nombre'], comuna = self.comuna1, partido = self.data_candidato[0]['partido'], web = self.data_candidato[0]['web'])
		self.candidato2 = Candidato.objects.create(nombre=self.data_candidato[1]['nombre'], comuna = self.comuna1, partido = self.data_candidato[1]['partido'])
		self.candidato3 = Candidato.objects.create(nombre=self.data_candidato[2]['nombre'], comuna = self.comuna2, partido = self.data_candidato[2]['partido'])
		self.question1 = "Why can't we be friends?"
		self.answer1 = "I'd kinda like to be the President, so I can show you how your money's spent"
		self.question2 = 'Who let the dogs out?'
		self.answer2 = 'woof, woof, woof, woof'
		self.template = '<h3>Hello, this is a test template</h3><br><p>Message goes here</p>'
		self.mail_user = 'mailer@'
		self.mail_pass = ''

	def test_create_candidate(self):

		self.assertTrue(self.candidato1)
		self.assertEquals(self.candidato1.nombre, 'candidato1')
		self.assertEquals(self.candidato1.comuna, self.comuna1)
		self.assertEquals(self.candidato1.partido, 'partido1')
		self.assertEquals(self.candidato1.web, 'web1')
	
	def test_create_contacto(self):
		contacto, created = Contacto.objects.get_or_create(tipo = 1, valor = 'test@test.com', candidato = self.candidato1)
		self.assertTrue(created)
		self.assertEquals(contacto.tipo, 1)
		self.assertEquals(contacto.valor, 'test@test.com')
		self.assertEquals(contacto.candidato, self.candidato1)
		self.assertTrue(contacto)

	def test_create_question_message(self):
		#Se crea la pregunta y las respuestas asociadas
		pregunta = Pregunta.objects.create(
											remitente='remitente1', 
											texto_pregunta='texto_pregunta1')
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta, candidato=self.candidato2)
		#Se crea la pregunta con su respectivo texto y remitente?
		self.assertTrue(pregunta)
		self.assertEquals(pregunta.aprobada,False)
		self.assertEquals(pregunta.texto_pregunta,'texto_pregunta1')
		self.assertEquals(pregunta.remitente,'remitente1')
		#Se crearon las respuestas asociadas a la pregunta?
		respuesta_no_contestada1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta)[0]
		respuesta_no_contestada2 = Respuesta.objects.filter(candidato=self.candidato2).filter(pregunta=pregunta)[0]
		#Se crean las respuestas, y se guardan en la bd con los valores iniciales que corresponden?
		self.assertEquals(respuesta_no_contestada1.texto_respuesta,'Sin Respuesta')
		self.assertEquals(respuesta_no_contestada2.texto_respuesta,'Sin Respuesta')
		#Existe la asociación entre preguntas y candidatos?
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).filter(nombre=self.candidato1.nombre).count(),1)
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).filter(nombre=self.candidato2.nombre).count(),1)
		#Sólo se agregó la pregunta a 2 candidatos?
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta).count(),2)


		

	def test_create_answer_message(self):
		#Se crea la pregunta y las respuestas asociadas
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta1, candidato=self.candidato2)
		pregunta2 = Pregunta.objects.create(texto_pregunta='texto_pregunta2', remitente='remitente2')
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta2, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta2, candidato=self.candidato2)
		#Se cambia la respuesta por defecto a la respuesta obtenida?
		respuesta_candidato1_pregunta1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta1)[0]
		respuesta_candidato1_pregunta1.texto_respuesta ='texto_candidato1_respuesta1'
		respuesta_candidato1_pregunta1.save()
		respuesta_candidato1_pregunta1_db = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta1)[0]
		self.assertEquals(respuesta_candidato1_pregunta1_db.texto_respuesta,'texto_candidato1_respuesta1')
		#Se cambian accidentalmente otras respuestas?
		respuesta_candidato1_pregunta2 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta2)[0]
		self.assertEquals(respuesta_candidato1_pregunta2.texto_respuesta,'Sin Respuesta')
	
	def test_mail_sending(self):

		# Send message.
		mail.send_mail('Subject here', 'Here is the message.','from@example.com', ['to@example.com'],
		    fail_silently=False)

		# Test that one message has been sent.
		self.assertEqual(len(mail.outbox), 1)

		# Verify that the subject of the first message is correct.
		self.assertEqual(mail.outbox[0].subject, 'Subject here')
		#chequear que el mail llega y lo podemos traer


	def test_get_question_page(self):
		url = reverse('comuna-preguntales', kwargs={'slug':self.comuna1.slug})
		response = self.client.post(url)

		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'municipales2012/preguntales.html')
		self.assertTrue('form' in response.context)
		choices = response.context['form'].fields['candidato'].choices
		self.assertTrue((self.candidato1.pk, self.candidato1.nombre) in response.context['form'].fields['candidato'].choices)
		self.assertTrue((self.candidato2.pk, self.candidato2.nombre) in response.context['form'].fields['candidato'].choices)
		self.assertTrue((self.candidato3.pk, self.candidato3.nombre) not in response.context['form'].fields['candidato'].choices)





	def test_submit_question_message(self):

		
		#hackeamos .virtualenvs/mun12/lib/python2.7/site-packages/captcha/fields.py porque no consideraba settings.debug como true.
		#Post data
		url = reverse('comuna-preguntales', kwargs={'slug':self.comuna1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})
		self.assertEquals(Pregunta.objects.count(), 1)
		self.assertEquals(Pregunta.objects.all()[0].texto_pregunta, 'Texto Pregunta')
		self.assertEquals(Pregunta.objects.all()[0].remitente, 'Remitente 1')

		self.assertEquals(Respuesta.objects.count(), 2)



		#Se crea la pregunta con su respectivo texto y remitente
		pregunta_enviada = Pregunta.objects.filter(candidato=self.candidato1).filter(remitente='Remitente 1')[0]
		self.assertTrue(pregunta_enviada)
		self.assertEquals(pregunta_enviada.texto_pregunta,'Texto Pregunta')
		self.assertEquals(pregunta_enviada.remitente,'Remitente 1')
		#Se crean las respuestas, y se guardan en la bd con los valores iniciales que corresponden
		respuesta_no_contestada1 = Respuesta.objects.filter(candidato=self.candidato1).filter(pregunta=pregunta_enviada)[0]
		respuesta_no_contestada2 = Respuesta.objects.filter(candidato=self.candidato2).filter(pregunta=pregunta_enviada)[0]
		self.assertEquals(respuesta_no_contestada1.texto_respuesta,'Sin Respuesta')
		self.assertEquals(respuesta_no_contestada2.texto_respuesta,'Sin Respuesta')
		#Existe la asociación entre preguntas y candidatos
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).filter(nombre=self.candidato1.nombre).count(),1)
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).filter(nombre=self.candidato2.nombre).count(),1)
		#Sólo se agregó la pregunta a 2 candidatos
		self.assertEquals(Candidato.objects.filter(pregunta=pregunta_enviada).count(),2)
	
	def test_send_question_message(self):

		
		#hackeamos .virtualenvs/mun12/lib/python2.7/site-packages/captcha/fields.py porque no consideraba settings.debug como true.
		#Post data
		contacto1, created = Contacto.objects.get_or_create(tipo = 1, valor = 'candidato1@candidato1.com', candidato = self.candidato1)
		contacto2, created = Contacto.objects.get_or_create(tipo = 1, valor = 'candidato2@candidato2.com', candidato = self.candidato2)
		url = reverse('comuna-preguntales', kwargs={'slug':self.comuna1.slug})
		response = self.client.post(url, {'candidato': [self.candidato1.pk, self.candidato2.pk],
											'texto_pregunta': 'Texto Pregunta', 
											'remitente': 'Remitente 1',
											'recaptcha_response_field': 'PASSED'})
		pregunta_nueva = Pregunta.objects.get(remitente='Remitente 1')
		pregunta_nueva.enviar()
		# Test that one message has been sent.
		self.assertEqual(len(mail.outbox), 2)

		# Verify that the subject of the first message is correct.
		self.assertEqual(mail.outbox[0].subject, 'Un ciudadano está interesado en más información sobre tu candidatura')
		self.assertEqual(mail.outbox[1].subject, 'Un ciudadano está interesado en más información sobre tu candidatura')
		# self.assertEqual(mail.outbox[0].from, 'municiaples2012@votainteligente.cl')
		# self.assertEqual(mail.outbox[1].from, 'municiaples2012@votainteligente.cl')
		#chequear que el mail llega y lo podemos traer


	def test_display_conversations(self):
		
		url = reverse('comuna-preguntales', kwargs={'slug':self.comuna1.slug})
		response = self.client.get(url)
		
		pregunta1 = Pregunta.objects.create(texto_pregunta='texto_pregunta1', remitente='remitente1')
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta1, candidato=self.candidato1)
		Respuesta.objects.create(texto_respuesta = 'Sin Respuesta', pregunta=pregunta1, candidato=self.candidato2)

		self.assertEquals(response.status_code, 200)
		#Check conversaciones
		self.assertTrue('conversaciones' in response.context)
		#Conversaciones aren't displayed if not allowed
		self.assertEquals(response.context['conversaciones'], {})
		#Conversaciones are displayed if allowed
		pregunta = Pregunta.objects.filter(candidato=self.candidato1).filter(remitente='remitente1')[0]
		pregunta.aprobada = True
		pregunta.save()
		response = self.client.get(url)
		conversaciones = response.context['conversaciones']
		nombre_remitente, pregunta = conversaciones.popitem()
		texto_pregunta, respuestas = pregunta.popitem()
		candidato, texto_respuesta = respuestas.popitem()
		self.assertTrue(nombre_remitente)
		self.assertTrue(texto_pregunta)
		self.assertTrue(candidato)
		self.assertTrue(texto_respuesta)
	

	#def test_create_mail_template(self):
		
	# def test_create_question_mail(self):
	# 	import imaplib
	# 	connection = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	# 	connection.login(user, pass)
'''
	def test_send_question_mail(self):
		
	def test_save_question_mail(self):
		
	def test_retrieve_question_mail(self):
		
	def test_obtain_answer_mail(self):
		
	def test_save_answer_mail(self):
		
	def test_retrieve_answer_mail(self):
		
	def test_associate_question_answer(self):
		
	def test_display_questions_answers(self):
		
	def test_calculate_response_stats(self):
	
'''	
class ContactosLoaderTestCase(TestCase):
	def setUp(self):
		self.line1 = ["FIERA FEROZ","Algarrobo","fieripipoo@ciudadanointeligente.cl"]
		self.line2 = ["FIERA FEROZ INTELIGENTE","Algarrobo","este no es el mail de la Fiera"]
		self.line3 = ["FIERA FEROZ INTELIGENTE","Algarrobo",""]
		self.lines = [self.line1, self.line2]

		self.algarrobo = Comuna.objects.create(nombre=u"Algarrobo", slug=u"algarrobo")
		self.candidateloader = ContactosLoader()

	def test_create_detect_candidate(self):
		
		candidate = self.candidateloader.detectCandidate(self.line1)

		self.assertEquals(candidate.nombre, u"FIERA FEROZ")
		self.assertEquals(candidate.comuna, self.algarrobo)

	def test_detect_contacto(self):
		candidate = self.candidateloader.detectCandidate(self.line1)
		contacto = self.candidateloader.detectContacto(self.line1)

		self.assertEquals(contacto.valor, u"fieripipoo@ciudadanointeligente.cl")
		self.assertEquals(contacto.candidato, candidate)


	def test_does_not_create_contacto_if_it_isnt_a_mail(self):
		contacto = self.candidateloader.detectContacto(self.line2)

		self.assertTrue(contacto is None)
		self.assertEquals(len(self.candidateloader.failed),1)
		self.assertEquals(self.candidateloader.failed[0],{u"Algarrobo",u"FIERA FEROZ INTELIGENTE",u"este no es el mail de la Fiera"})

	def test_does_not_create_two_candidates(self):
		previous_candidate = Candidato.objects.create(nombre=u"FIERA FEROZ", comuna=self.algarrobo, partido=u"Partido Feroz")
		contacto = self.candidateloader.detectContacto(self.line1)

		self.assertEquals(Candidato.objects.all().count(), 1)

	def test_empty_emails_do_not_belong_to_fail(self):
		contacto = self.candidateloader.detectContacto(self.line3)
		self.assertTrue(contacto is None)

		self.assertEquals(len(self.candidateloader.empty),1)
		self.assertEquals(self.candidateloader.empty[0],{u"Algarrobo",u"FIERA FEROZ INTELIGENTE"})


	def test_it_does_not_create_two_candidates(self):

		contacto = self.candidateloader.detectContacto(self.line2)
		contacto = self.candidateloader.detectContacto(self.line2)

		self.assertEquals(Candidato.objects.all().count(), 1)








	##TODO: Testear la clase command y el metodo handle sin crear conflicto con la otra clase
	##Command del comunas_importer


class CandidatoLoader(TestCase):
	def setUp(self):
		self.line1 = ["Algarrobo","FIERA FEROZ","Partido Feroz"]
		self.line2 = ["Algarrobo","FIERA FEROZ INTELIGENTE","Lavate los dientes"]
		self.lines = [self.line1, self.line2]
		self.algarrobo = Comuna.objects.create(nombre=u"Algarrobo", slug=u"algarrobo")
		self.candidateloader = CandidatosLoader()

	
	def test_crea_candidato(self):
		candidate = self.candidateloader.detectCandidate(self.line1)

		self.assertEquals(candidate.nombre, u"FIERA FEROZ")
		self.assertEquals(candidate.partido, u"Partido Feroz")
		self.assertEquals(candidate.comuna, self.algarrobo)


	def test_detecta_la_comuna(self):
		comuna = self.candidateloader.detectComuna(self.line1)


		self.assertEquals(comuna.nombre, u"Algarrobo")
		self.assertEquals(comuna.slug, u"algarrobo")

	def test_it_does_not_create_two_candidates(self):

		contacto = self.candidateloader.detectCandidate(self.line2)
		contacto = self.candidateloader.detectCandidate(self.line2)

		self.assertEquals(Candidato.objects.all().count(), 1)


class CandidatosEstrellitas(TestCase):
	def setUp(self):
		self.comuna = Comuna.objects.create(nombre=u"La comuna", slug="la-comuna")
		self.candidato = Candidato.objects.create(nombre=u"Un candidato mala onda", partido=u"RN")


	def test_candidato_tres_estrellitas(self):
		#No hay contactos
		self.assertEquals(self.candidato.estrellitas, 3)

	def test_candidato_dos_estrellitas(self):
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"secretaria@rn.cl",tipo=2)

		self.assertEquals(self.candidato.estrellitas, 2)


	def test_candidato_una_estrella(self):
		contacto_personal = Contacto.objects.create(candidato=self.candidato, valor=u"secretaria@rn.cl",tipo=2)

		self.assertEquals(self.candidato.estrellitas, 1)









