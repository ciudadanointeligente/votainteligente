#encoding=UTF-8
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def uservoice_client_key():
    return settings.USERVOICE_CLIENT_KEY

@register.simple_tag
def disqus_short_name():
    return settings.DISQUS_SHORT_NAME

@register.simple_tag
def candidate_info_contact_mail():
    return settings.INFO_CONTACT_MAIL

@register.simple_tag
def candidate_info_contact_mail_subject():
    return settings.CANDIDATE_CONTACT_SUBJECT

@register.simple_tag
def ga_account_id():
    return settings.GOOGLE_ANALYTICS_TRACKER_ID

@register.simple_tag
def ga_account_domain():
    return settings.GOOGLE_ANALYTICS_DOMAIN