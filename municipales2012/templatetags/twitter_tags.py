from django import template

register = template.Library()


@register.filter(name='twittrespuesta')
def twittrespuesta(respuesta):
	return u""