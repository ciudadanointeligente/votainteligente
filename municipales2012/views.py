# -*- coding: utf-8 -*-#
# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import FormView
from models import Comuna, Indice, Pregunta, Candidato, Respuesta, Contacto
from django.shortcuts import get_object_or_404
from forms import PreguntaForm
from django.core.urlresolvers import reverse
from django.contrib import messages

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
		comunas = Comuna.objects.all()
		context['indices'] = indices
		context['title'] = self.object.nombre
		context['comunas'] = comunas
		return context


class ComunaIndices(DetailView):
	model = Comuna

	def get_template_names(self):
		return ['municipales2012/todos_los_indices.html']

	def get_context_data(self, **kwargs):
		context = super(ComunaIndices, self).get_context_data(**kwargs)
		indices = self.object.indice_set.all()
		comunas = Comuna.objects.all()
		context['indices'] = indices
		context['title'] = self.object.nombre + u" índices detallados"
		context['comunas'] = comunas
		return context

class ComunaPreguntales(CreateView):
	#model = Pregunta
	form_class = PreguntaForm
	#template_name = 'municipales2012/preguntales.html'
	success_url = 'preguntales'

	def get_template_names(self):
		return ['municipales2012/preguntales.html']

	def get_context_data(self, **kwargs):
		comuna_slug = self.kwargs['slug']
		comuna = get_object_or_404(Comuna, slug = comuna_slug)
		context = super(ComunaPreguntales, self).get_context_data(**kwargs)
		candidatos_comuna = Candidato.objects.filter(comuna = comuna)
		contactos_candidato = Contacto.objects.filter(candidato__in = candidatos_comuna)
		candidatos = candidatos_comuna.filter(contacto__in = contactos_candidato)
		preguntas = Pregunta.objects.filter(candidato__in = candidatos_comuna).filter(aprobada = True)
		conversaciones = {}
		for pregunta in preguntas:
			texto_pregunta = pregunta.texto_pregunta
			mensaje = {}
			respuestas = {}
			respuestas_pregunta = Respuesta.objects.filter(pregunta=pregunta)
			for respuesta_pregunta in respuestas_pregunta:
				texto_respuesta = respuesta_pregunta.texto_respuesta
				nombre_candidato = respuesta_pregunta.candidato.nombre
				respuestas[nombre_candidato] = texto_respuesta
			nombre_emisor = pregunta.remitente
			mensaje[texto_pregunta] = respuestas
			conversaciones[nombre_emisor] = mensaje

		context['conversaciones'] = conversaciones
		context['candidatos'] = candidatos
		todas_las_comunas = Comuna.objects.all()
		context['comunas'] = todas_las_comunas
		context['comuna'] = comuna
		
		return context

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.save()
		url = reverse('comuna-preguntales', kwargs={'slug':self.kwargs['slug']})

		candidatos = form.cleaned_data['candidato']
		for candidato in candidatos:
			Respuesta.objects.create(candidato = candidato, pregunta = self.object)

     		messages.success(self.request, 'Tu pregunta ha sido enviada') 
     		
     		
		return HttpResponseRedirect(url)

	def get_form_kwargs(self):
		kwargs = super(ComunaPreguntales, self).get_form_kwargs()
		comuna_slug = self.kwargs['slug']
		comuna = get_object_or_404(Comuna, slug = comuna_slug)
		kwargs['comuna'] = comuna
		return kwargs

class MetodologiaView(TemplateView):
	template_name="municipales2012/metodologia.html"

	def get_context_data(self, **kwargs):
		context = super(MetodologiaView, self).get_context_data(**kwargs)
		context['title'] = u"Metodología"
		comunas = Comuna.objects.all()
		context['comunas'] = comunas
		return context


class QuePuedoHacerHacerView(TemplateView):
	template_name = "municipales2012/que_puedo_hacer.html"

	def get_context_data(self, **kwargs):
		context = super(QuePuedoHacerHacerView, self).get_context_data(**kwargs)
		context['title'] = u"¿Qué puedo hacer?"
		comunas = Comuna.objects.all()
		context['comunas'] = comunas
		return context


class QuienesSomosView(TemplateView):
	template_name="municipales2012/quienesSomos.html"

	def get_context_data(self, **kwargs):
		context = super(QuienesSomosView, self).get_context_data(**kwargs)
		context['title'] = u"Quienes somos"
		comunas = Comuna.objects.all()
		context['comunas'] = comunas
		return context


class ReportaView(TemplateView):
	template_name="municipales2012/reporta.html"

	def get_context_data(self, **kwargs):
		context = super(ReportaView, self).get_context_data(**kwargs)
		context['title'] = u"Fiscaliza"
		comunas = Comuna.objects.all()
		context['comunas'] = comunas
		return context
