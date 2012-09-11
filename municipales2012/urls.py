from django.conf.urls import patterns, include, url
from views import HomeTemplateView, ComunaOverview, ComunaIndices

urlpatterns = patterns('',
	url(r'^$', HomeTemplateView.as_view(template_name="home.html"), name="home"),
	url(r'^(?P<slug>[-\w]+)/indices/?', ComunaIndices.as_view(), name='comuna-index-detail'),
	url(r'^(?P<slug>[-\w]+)/?', ComunaOverview.as_view(), name="comuna-overview"),
	
	)