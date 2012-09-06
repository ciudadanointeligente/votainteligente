from django.conf.urls import patterns, include, url
from views import HomeTemplateView

urlpatterns = patterns('',
	url(r'^/?', HomeTemplateView.as_view(template_name="home.html"), name="home")
	)