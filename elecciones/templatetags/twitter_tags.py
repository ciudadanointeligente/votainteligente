# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.contrib.sites.models import Site

import socket

# try:
#     host_name = socket.getfqdn()
# except:
#     host_name = 'localhost'

register = template.Library()

# @register.simple_tag
# def host_name():
# 	return settings.HOSTNAME


@register.filter(name='twittrespuesta')
def twittrespuesta(respuesta):
	if not respuesta.candidato.twitter:
		return u""
	template = Template("{{ request.get_host }}")
	url_respuesta = respuesta.get_absolute_url()
	anchor = '<a href="https://twitter.com/intent/tweet?screen_name='+respuesta.candidato.twitter + '&text=Yo%20tambien%20quiero%20saber%20tu%20opinion%20sobre%20este%20tema&url=' + template.render(Context())+url_respuesta+ '" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Insiste con @'+respuesta.candidato.twitter+'</a>'
	return mark_safe(anchor)


@register.filter(name='no_responde')
def no_responde(malo):	
	if not malo["candidato"].twitter:
		return u""

	url_preguntales = reverse('eleccion-preguntales', kwargs={
			'slug':malo["candidato"].eleccion.slug
			})
	domain_url = Site.objects.get_current().domain
	anchor = u'<a href="https://twitter.com/intent/tweet" data-text="'+str(malo["preguntas_no_respondidas"])+u' preguntas de ciudadanos no han sido respondidas por @'+malo["candidato"].twitter+u', revisalas en http://'+domain_url+url_preguntales+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+malo["candidato"].twitter+u'</a>'
	return mark_safe(anchor)


@register.filter(name='si_responde')
def si_responde(bueno):	
	if not bueno["candidato"].twitter:
		return u""

	url_preguntales = reverse('eleccion-preguntales', kwargs={
			'slug':bueno["candidato"].eleccion.slug
			})
	domain_url = Site.objects.get_current().domain
	anchor = u'<a href="https://twitter.com/intent/tweet" data-text="Gracias @'+bueno["candidato"].twitter+u' por responder a los ciudadanos en http://'+domain_url+url_preguntales+u'" class="twitter-mention-button" data-lang="es" data-related="ciudadanoi">Tweet to @'+bueno["candidato"].twitter+u'</a>'
	return mark_safe(anchor)
