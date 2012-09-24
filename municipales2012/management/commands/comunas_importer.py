# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
import csv
from municipales2012.models import Comuna, Area, Indice, Dato

class CsvReader(object):
	def detectComuna(self,line):
		nombre = line[0]
		nombre = nombre.decode('utf-8')
		nombre = nombre.strip()
		comuna, created = Comuna.objects.get_or_create(nombre=nombre, slug=slugify(nombre))
		return comuna

	def detectArea(self, line):
		nombre_area = line[1]
		nombre_area = nombre_area.decode('utf-8')
		nombre_area = nombre_area.strip()
		area, created = Area.objects.get_or_create(nombre=nombre_area)
		return area

	def detectDato(self, line):
		dato, created = Dato.objects.get_or_create(nombre=line[2].strip())
		return dato


	def detectIndice(self, line):

		comuna = self.detectComuna(line)
		area = self.detectArea(line)
		dato = self.detectDato(line)

		try:
			indice = Indice.objects.get(
				comuna=comuna,
				dato=dato
				)
			indice.encabezado = line[3].strip()
			indice.numero_1 = line[4].strip()
			indice.texto_1 = line[5].strip()
			indice.numero_2 = line[6].strip()
			indice.texto_2 = line[7].strip()
			indice.texto_pie_pagina_1 = line[8].strip()
			indice.numero_pie_pagina_1 = line[9].strip()
			indice.texto_pie_pagina_2 = line[10].strip()
			indice.save()
		except:
			indice = Indice.objects.create(
				comuna = comuna,
				area = area,
				dato = dato,
				encabezado = line[3].strip(),
				numero_1 = line[4].strip(),
				texto_1 = line[5].strip(),
				numero_2 = line[6].strip(),
				texto_2 = line[7].strip(),
				texto_pie_pagina_1 = line[8].strip(),
				numero_pie_pagina_1 = line[9].strip(),
				texto_pie_pagina_2 = line[10].strip(),
				en_carrusel = True
				)


		
		return indice


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')
        csvReader = CsvReader()
        for line in reader:
            indice = csvReader.detectIndice(line)
            nombre_comuna = line[0].decode('utf-8').strip()
            nombre_area = line[1].decode('utf-8').strip()
            nombre_dato = line[2].decode('utf-8').strip()
            print u"Comuna: "+ nombre_comuna+u" | Area: "+nombre_area+u" | Dato: "+nombre_dato