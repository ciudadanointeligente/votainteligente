from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter(name='twittrespuesta')
def twittrespuesta(respuesta):
	if not respuesta.candidato.twitter:
		return u""

	url_respuesta = respuesta.get_absolute_url()
	anchor = u'<a href="https://twitter.com/intent/tweet?screen_name='+respuesta.candidato.twitter+u'" data-text="http://www.votainteligente.cl'+url_respuesta+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+respuesta.candidato.twitter+u'</a>'
	return mark_safe(anchor)


@register.filter(name='no_responde')
def no_responde(candidato):	
	if not candidato.twitter:
		return u""

	url_preguntales = reverse('comuna-preguntales', kwargs={
			'slug':candidato.comuna.slug
			})
	anchor = u'<a href="https://twitter.com/intent/tweet?screen_name='+candidato.twitter+u'" data-text="Las preguntas de sus ciudadanos en http://www.votainteligente.cl'+url_preguntales+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+candidato.twitter+u'</a>'
	return mark_safe(anchor)
