# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic import TemplateView, DetailView
from models import Comuna, Indice

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

class MetodologiaView(TemplateView):
	template_name="municipales2012/metodologia.html"

	def get_context_data(self, **kwargs):
		return {"title":u'Metodología'}


class QuienesSomosView(TemplateView):
	template_name="municipales2012/quienesSomos.html"

	def get_context_data(self, **kwargs):
		return {'title': u"Quienes somos"}