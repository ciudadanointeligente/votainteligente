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
		return context


class ComunaIndices(DetailView):
	model = Comuna

	def get_template_names(self):
		return ['municipales2012/todos_los_indices.html']

	def get_context_data(self, **kwargs):
		context = super(ComunaIndices, self).get_context_data(**kwargs)
		indices = self.object.indice_set.all()
		context['indices'] = indices
		return context