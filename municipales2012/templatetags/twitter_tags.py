from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='twittrespuesta')
def twittrespuesta(respuesta):
	if respuesta.candidato.twitter is None:
		return u""

	url_respuesta = respuesta.get_absolute_url()
	anchor = u'<a href="https://twitter.com/intent/tweet?screen_name="'+respuesta.candidato.twitter+u'" class="twitter-mention-button" data-lang="es">http://www.votainteligente.cl'+url_respuesta+u'</a>'
	return mark_safe(anchor)