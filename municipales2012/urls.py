from django.conf.urls import patterns, include, url
from views import HomeTemplateView, ComunaOverview, ComunaIndices
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', HomeTemplateView.as_view(template_name="home.html"), name="home"),
	

	#static pages
	url(r'^metodologia/?$', TemplateView.as_view(template_name="municipales2012/metodologia.html"), name="metodologia"),
	url(r'^somos/?$', TemplateView.as_view(template_name="municipales2012/quienesSomos.html"), name="somos"),
	

	#pages depending on the comuna
	url(r'^(?P<slug>[-\w]+)/indices/?$', ComunaIndices.as_view(), name='comuna-index-detail'),
	url(r'^(?P<slug>[-\w]+)/?$', ComunaOverview.as_view(), name="comuna-overview"),
	
	)