# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic import TemplateView, DetailView
from models import Comuna, Indice
from django.core.urlresolvers import reverse

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
		context['full_path'] = self.request.build_absolute_uri()
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
		url_comuna = reverse('comuna-overview', kwargs={
			'slug':self.object.slug
			})
		context['full_path'] = self.request.build_absolute_uri(url_comuna)
		
		return context

class MetodologiaView(TemplateView):
	template_name="municipales2012/metodologia.html"

	def get_context_data(self, **kwargs):
		context = super(MetodologiaView, self).get_context_data(**kwargs)
		context['title'] = u"Metodología"
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