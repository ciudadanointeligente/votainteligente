from municipales2012.models import Comuna
from django import template

register = template.Library()

def comunas_search():
	comunas = Comuna.objects.all()
	return {'comunas':comunas}

register.inclusion_tag('comunas_search.html')(comunas_search)