# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView
from models import Comuna, Indice, Pregunta
from django.shortcuts import get_object_or_404

class HomeTemplateView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		comunas = Comuna.objects.all()

		context['comunas'] = comunas
		return context

class ComunaOverview(DetailView):
	model = Comuna

	def get_context_data(self, **kwargs):
		context = super(ComunaOverview, self).get_context_data(**kwargs)
		indices = self.object.indice_set.filter(en_carrusel=True)
		context['indices'] = indices
		context['title'] = self.object.nombre
		return context


class ComunaIndices(DetailView):
	model = Comuna

	def get_template_names(self):
		return ['municipales2012/todos_los_indices.html']

	def get_context_data(self, **kwargs):
		context = super(ComunaIndices, self).get_context_data(**kwargs)
		indices = self.object.indice_set.all()
		context['indices'] = indices
		context['title'] = self.object.nombre + u" índices detallados"
		return context

class ComunaPreguntales(CreateView):
	model = Pregunta

	def get_template_names(self):
		return ['municipales2012/todos_los_indices.html']

	def get_context_data(self, **kwargs):
		comuna_slug = self.kwargs['slug']
		comuna = get_object_or_404(Comuna, slug = comuna_slug)
		context = super(ComunaIndices, self).get_context_data(**kwargs)
		preguntas = self.object.pregunta_set.all()
		conversaciones = {}
		for pregunta in preguntas:
			texto_pregunta = pregunta.texto_pregunta
			respuestas = {}
			respuestas_pregunta = Respuestas.objects.filter(pregunta=pregunta)
			for respuesta_pregunta in respuestas_pregunta:
				texto_respuesta = respuesta_pregunta.texto_respuesta
				nombre_candidato = respuesta_pregunta.candidato.nombre
				respuestas[nombre_candidato] = texto_respuesta
			nombre_emisor = pregunta.remitente
			mensaje[nombre_emisor] = texto_pregunta
			conversaciones[mensaje] = respuestas

		context['conversaciones'] = conversaciones
		context['candidatos'] = candidatos
		context['title'] = "Preguntas a los Candidatos de " + comuna.nombre
		
		return context

class MetodologiaView(TemplateView):
	template_name="municipales2012/metodologia.html"

	def get_context_data(self, **kwargs):
		return {"title":u'Metodología'}


class QuienesSomosView(TemplateView):
	template_name="municipales2012/quienesSomos.html"

	def get_context_data(self, **kwargs):
		return {'title': u"Quienes somos"}