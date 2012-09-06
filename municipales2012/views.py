# Create your views here.
from django.views.generic import TemplateView
from models import Comuna

class HomeTemplateView(TemplateView):
	def get_context_data(self, **kwargs):
		context = super(HomeTemplateView, self).get_context_data(**kwargs)
		comunas = Comuna.objects.all()
		context['comunas'] = comunas
		return context
