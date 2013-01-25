from django.test import TestCase
from django.template import Template, Context
from django.conf import settings

class SettingsVariablesInTemplate(TestCase):
	def setUp(self):
		pass

	def test_it_provides_uservoice_template_tag(self):
		settings.USERVOICE_CLIENT_KEY = "USERVOICE KEY"
		template = Template('{% load settingsvars_tags %}{% uservoice_client_key %}')
		self.assertEqual(template.render(Context({})), "USERVOICE KEY")

	def test_it_provides_google_analytics_template_tag(self):
		settings.GOOGLE_ANALYTICS_TRACKER_ID = "GOOGLE ANALYTICS ACCOUNT ID"
		settings.GOOGLE_ANALYTICS_DOMAIN = "testdomain.com"
		template = Template('{% load settingsvars_tags %}{% ga_account_id %} - {% ga_account_domain %}')
		self.assertEqual(template.render(Context({})), "GOOGLE ANALYTICS ACCOUNT ID - testdomain.com")

	def test_it_provides_disqus_short_name_template_tag(self):
		settings.DISQUS_SHORT_NAME = "DISQUS_SHORT_NAME"
		template = Template('{% load settingsvars_tags %}{% disqus_short_name %}')
		self.assertEqual(template.render(Context({})), "DISQUS_SHORT_NAME")

	def test_it_provides_mail_subject_template_tag(self):
		settings.CANDIDATE_CONTACT_SUBJECT = "Mail Subject"
		template = Template('{% load settingsvars_tags %}{% candidate_info_contact_mail_subject %}')
		self.assertEqual(template.render(Context({})), "Mail Subject")

	def test_it_provides_mail_address_template_tag(self):
		settings.CANDIDATE_INFO_CONTACT_MAIL = "candidatos@mail.com"
		template = Template('{% load settingsvars_tags %}{% candidate_info_contact_mail %}')
		self.assertEqual(template.render(Context({})), "candidatos@mail.com")