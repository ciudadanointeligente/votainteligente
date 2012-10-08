# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from municipales2012.models import Candidato, Comuna, Contacto
from django.core.validators import email_re
import csv


class ContactosLoader:
	def __init__(self):
		self.failed = []
		self.empty = []

	def detectCandidate(self, line):
		nombre_candidato = line[0].decode('utf-8').strip()
		nombre_comuna = line[1].decode('utf-8').strip()
		comuna, created = Comuna.objects.get_or_create(nombre=nombre_comuna)
		candidato, created = Candidato.objects.get_or_create(nombre=nombre_candidato, comuna=comuna)
		return candidato

	def detectContacto(self, line):
		candidato = self.detectCandidate(line)
		valor = line[2].decode('utf-8').strip()
		if not valor:
			empty_data = {
				candidato.comuna.nombre,
				candidato.nombre
			}
			self.empty.append(empty_data)
			return None

		if email_re.match(valor):

			contacto, created = Contacto.objects.get_or_create(valor=valor, candidato=candidato)
			return contacto
		failed_data = {
			candidato.comuna.nombre,
			candidato.nombre,
			valor
		}
		self.failed.append(failed_data)
		return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')

        contactos_loader = ContactosLoader()
        for line in reader:
            contacto = contactos_loader.detectContacto(line)
            if contacto is not None:
            	print u"Comuna: "+ contacto.candidato.comuna.nombre+u" | Candidato: "+contacto.candidato.nombre\
            	+u" | Contacto: "+contacto.valor

        print u"Los siguientes contactos no pudieron ser ingresados"
        for contacto in contactos_loader.failed:
        	print contacto[0], contactos[1], contacto[2]

        print u"Los siguientes contactos están vacíos"
        for contacto in contactos_loader.empty:
        	print contacto[0], contacto[1]