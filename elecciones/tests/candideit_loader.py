# -*- coding: utf-8 -*-

from django.test import TestCase
from elecciones.models import Eleccion, Candidato
from elecciones.management.commands.candideit_importer import *
from elecciones.management.commands import candideit_importer
import json
from ludibrio import Stub
import slumber
from slumber import Resource
import encodings.idna


class CandideitLoaderTestCase(TestCase):
    def setUp(self):
        response_json = open("elecciones/tests/candideit_api_response.json")
        self.parsed_elections = json.load(response_json)
        self.username = "fiera"
        self.api_key = "keyfiera"
        self.syncronizer = Syncronizer(self.username, self.api_key)
        with Stub() as api:
            api.election.get(username=self.username, api_key=self.api_key,offset=0) >> self.parsed_elections
        #Here is where I mock the api
        self.syncronizer.api = api




    def test_syncronize_elections(self):
        
        self.syncronizer.sync_elections()

        #Now there should be an election

        elections = Eleccion.objects.all()

        self.assertEquals(elections.count(), 1)
        self.assertEquals(elections[0].nombre, u"asdasdfggggggggga")
        self.assertEquals(elections[0].slug, u"asdasdfggggggggga")
        self.assertEquals(elections[0].main_embedded, u"http://example.com/lfalvarez/asdasdfgggggggggggga/embeded")

    def test_it_does_not_create_two_elections_with_the_same_name(self):
        self.syncronizer.sync_elections()
        self.syncronizer.sync_elections()

        self.assertEquals(Eleccion.objects.count(), 1)        


    def test_syncronize_candidates(self):
        election = Eleccion.objects.create(nombre="laeleccion")
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])

        self.assertEquals(Candidato.objects.filter(eleccion=election).count(), 2)
        self.assertEquals(Candidato.objects.get(nombre=u"cand 1").eleccion, election)
        self.assertEquals(Candidato.objects.get(nombre=u"cand 2").eleccion, election)


    def test_it_does_not_create_twice_a_candidate(self):
        election = Eleccion.objects.create(nombre="laeleccion")
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])
        self.syncronizer.sync_candidates(election, self.parsed_elections["objects"][0]["candidates"])

        self.assertEquals(Candidato.objects.filter(eleccion=election).count(), 2)


    def test_syncronize_both(self):
        self.syncronizer.sync_elections()

        self.assertEquals(Candidato.objects.all().count(), 2)
        self.assertEquals(Candidato.objects.filter(nombre=u"cand 1").count(), 1)
        self.assertEquals(Candidato.objects.filter(nombre=u"cand 2").count(), 1)

    def test_it_loads_several_pages(self):
        response_json_1 = open("elecciones/tests/big_json_1.json")
        response_json_2 = open("elecciones/tests/big_json_2.json")
        parsed_elections_1 = json.load(response_json_1)
        parsed_elections_2 = json.load(response_json_2)
        username = "fiera"
        api_key = "keyfiera"
        syncronizer = Syncronizer(username, api_key)
        with Stub() as api:
            api.election.get(username=self.username, api_key=self.api_key,offset=0) >> parsed_elections_1
            api.election.get(username=self.username, api_key=self.api_key,offset=20) >> parsed_elections_2

        #Here is where I mock the api
        syncronizer.api = api

        syncronizer.sync_elections()
        self.assertEquals(Eleccion.objects.count(), 26)


        
