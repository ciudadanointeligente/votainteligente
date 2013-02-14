from elecciones.models import Eleccion
from django import template

register = template.Library()

def elecciones_search():
	elecciones = Eleccion.objects.all()
	return {'elecciones':elecciones}

register.inclusion_tag('elecciones_search.html')(elecciones_search)