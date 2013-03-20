# -*- coding: utf-8 -*-

from elecciones.models import Eleccion, Candidato
import slumber
from django.core.management.base import BaseCommand, CommandError

class Syncronizer(object):
    def __init__(self, username, api_key, base_url="candideit.org"):
        self.api = slumber.API("http://"+base_url+"/api/v1/")
        self.username = username
        self.api_key = api_key

    def sync_elections(self):
        next = True
        offset=0
        while next:
            parsed_elections = self.api.election.get(username=self.username, api_key=self.api_key, offset=offset)
            next = parsed_elections["meta"]["next"]
            offset = parsed_elections["meta"]["offset"] + parsed_elections["meta"]["limit"]
            for election_dict in parsed_elections["objects"]:
                election, created = Eleccion.objects.get_or_create(nombre=election_dict["name"],\
                                        slug=election_dict["slug"],\
                                        main_embedded=election_dict["embedded_url"])
                self.sync_candidates(election, election_dict["candidates"])



    def sync_candidates(self, election, parsed_candidates):
        for candidate_dict in parsed_candidates:
            candidate, created = Candidato.objects.get_or_create(eleccion=election, nombre=candidate_dict["name"])


class Command(BaseCommand):
    args = '<username api_key>'
    help = 'Retrieves information from candideit.org api to populate this project'

    def handle(self, *args, **options):

        username = args[0]
        api_key = args[1]
        syncronizer = Syncronizer(username, api_key)
        syncronizer.sync_elections()
        # try:
        #     syncronizer.sync_elections()
        # except Exception:
        #     raise CommandError("Huston we had a problem")

        self.stdout.write('Success!')


