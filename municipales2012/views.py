# Create your views here.
from django.views.generic import TemplateView, DetailView
from models import Comuna, Region, Indice

class HomeTemplateView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		comunas = Comuna.objects.all()

		context['comunas'] = comunas
		regiones = Region.objects.all()
		context['regiones'] = regiones
		return context

class ComunaOverview(DetailView):
	model = Comuna

	def get_context_data(self, **kwargs):
		context = super(ComunaOverview, self).get_context_data(**kwargs)
		indices = Indice.objects.filter(comuna=self.object).filter(en_carrusel=True)
		context['indices'] = indices
		return context