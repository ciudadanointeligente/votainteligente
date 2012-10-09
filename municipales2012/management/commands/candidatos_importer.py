# coding= utf-8
from django.core.management.base import BaseCommand, CommandError
from municipales2012.models import Candidato, Comuna
import csv

class CandidatosLoader:
	def detectCandidate(self, line):
		comuna = self.detectComuna(line)
		nombre_candidato = line[1].decode('utf-8').strip()
		partido_candidato = line[2].decode('utf-8').strip()
		candidato, created = Candidato.objects.get_or_create(nombre=nombre_candidato, comuna=comuna, partido=partido_candidato)
		return candidato

	def detectComuna(self, line):
		nombre_comuna = line[0].decode('utf-8').strip()
		comuna, created = Comuna.objects.get_or_create(nombre=nombre_comuna)
		return comuna


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.reader(open(args[0], 'rb'), delimiter=',')

        candidatos_loader = CandidatosLoader()
        for line in reader:
            candidato = candidatos_loader.detectCandidate(line)
            if candidato is not None:
            	print u"Comuna: "+ candidato.comuna.nombre+u" | Candidato: "+candidato.nombre