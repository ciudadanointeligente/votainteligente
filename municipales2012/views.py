# -*- coding: utf-8 -*-#
# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormView
from models import Comuna, Indice, Pregunta, Candidato, Respuesta, Contacto
from django.shortcuts import get_object_or_404
from forms import PreguntaForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from operator import itemgetter
from django.db.models import Count

class HomeTemplateView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		comunas = Comuna.objects.all()

		context['comunas'] = comunas
		context['ultimas_preguntas']= Pregunta.objects.all().order_by('-id')[:5]
		context['ultimas_respuestas']= Respuesta.objects.exclude(texto_respuesta='Sin Respuesta').order_by('-id')[:5]
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

class NosFaltanDatosView(ListView):
	queryset = Candidato.sin_datos.all()
	context_object_name = "candidatos"

	def get_template_names(self):
		return ['municipales2012/nos_faltan_datos.html']

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
				nombre_candidato = respuesta_pregunta.candidato.nombre
				respuestas[nombre_candidato] = respuesta_pregunta
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



class Ranking(TemplateView):
	template_name = "municipales2012/ranking.html"

	def get_context_data(self, **kwargs):
		context = super(Ranking, self).get_context_data(**kwargs)
		context['malos'] = self.malos()
		context['buenos'] = self.buenos()
		return context

	def malos(self):
		clasificados = self.clasificados()
		return sorted(clasificados,  key=itemgetter('preguntas_no_respondidas'), reverse=True)

	def buenos(self):
		clasificados = self.clasificados()
		return sorted(clasificados,  key=itemgetter('preguntas_respondidas'), reverse=True)


	def clasificados(self):
		clasificados = []
		candidatos = Candidato.objects.all().annotate(preguntas_count=Count('pregunta')).exclude(preguntas_count=0)
		for candidato in candidatos:
			element = {
			'candidato':candidato,
			'pregunta_count':candidato.numero_preguntas(),
			'preguntas_respondidas':candidato.numero_respuestas(),
			'preguntas_no_respondidas':candidato.numero_preguntas() - candidato.numero_respuestas()
			}
			clasificados.append(element)

		return clasificados
