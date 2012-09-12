# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
import csv
from municipales2012.models import Comuna, Area, Indice, Dato

class CsvReader(object):
	def detectComuna(self,line):
		comuna, created = Comuna.objects.get_or_create(nombre=line[0], slug=slugify(line[0]))
		return comuna

	def detectArea(self, line):
		area, created = Area.objects.get_or_create(nombre=line[1])
		return area

	def detectDato(self, line):
		dato, created = Dato.objects.get_or_create(nombre=line[2])
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
			indice.encabezado = line[3]
			indice.numero_1 = line[4]
			indice.texto_1 = line[5]
			indice.numero_2 = line[6]
			indice.texto_2 = line[7]
			indice.texto_pie_pagina_1 = line[8]
			indice.numero_pie_pagina_1 = line[9]
			indice.texto_pie_pagina_2 = line[10]
			indice.save()
		except:
			indice = Indice.objects.create(
				comuna = comuna,
				area = area,
				dato = dato,
				encabezado = line[3],
				numero_1 = line[4],
				texto_1 = line[5],
				numero_2 = line[6],
				texto_2 = line[7],
				texto_pie_pagina_1 = line[8],
				numero_pie_pagina_1 = line[9],
				texto_pie_pagina_2 = line[10],
				en_carrusel = True
				)


		
		return indice


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')
        csvReader = CsvReader()
        for line in reader:
            indice = csvReader.detectIndice(line)