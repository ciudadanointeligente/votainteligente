from django.conf.urls import patterns, include, url
from views import HomeTemplateView, ComunaOverview, ComunaIndices, MetodologiaView, QuienesSomosView, ComunaPreguntales, ReportaView,\
QuePuedoHacerHacerView
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', HomeTemplateView.as_view(template_name="home.html"), name="home"),
	

	#static pages
	url(r'^metodologia/?$', MetodologiaView.as_view(), name="metodologia"),
	url(r'^somos/?$', QuienesSomosView.as_view(), name="somos"),
	url(r'^fiscaliza/?$', ReportaView.as_view(), name="reporta"),
	url(r'^que_puedo_hacer/?$', QuePuedoHacerHacerView.as_view(), name="que_puedo_hacer"),
	
	

	#pages depending on the comuna
	url(r'^(?P<slug>[-\w]+)/indices/?$', ComunaIndices.as_view(), name='comuna-index-detail'),
	url(r'^(?P<slug>[-\w]+)/?$', ComunaOverview.as_view(), name="comuna-overview"),
	url(r'^(?P<slug>[-\w]+)/preguntales/?$', ComunaPreguntales.as_view(), name="comuna-preguntales"),
	
	)
