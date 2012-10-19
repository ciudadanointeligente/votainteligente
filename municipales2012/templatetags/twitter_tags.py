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
def no_responde(malo):	
	if not malo["candidato"].twitter:
		return u""

	url_preguntales = reverse('comuna-preguntales', kwargs={
			'slug':malo["candidato"].comuna.slug
			})
	anchor = u'<a href="https://twitter.com/intent/tweet" data-text="'+str(malo["preguntas_no_respondidas"])+u' preguntas de ciudadanos no han sido respondidas por @'+malo["candidato"].twitter+u', revisalas en http://www.votainteligente.cl'+url_preguntales+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+malo["candidato"].twitter+u'</a>'
	return mark_safe(anchor)


@register.filter(name='si_responde')
def si_responde(bueno):	
	if not bueno["candidato"].twitter:
		return u""

	url_preguntales = reverse('comuna-preguntales', kwargs={
			'slug':bueno["candidato"].comuna.slug
			})
	anchor = u'<a href="https://twitter.com/intent/tweet" data-text="Gracias @'+bueno["candidato"].twitter+u' por responder a los ciudadanos en http://www.votainteligente.cl'+url_preguntales+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+bueno["candidato"].twitter+u'</a>'
	return mark_safe(anchor)
