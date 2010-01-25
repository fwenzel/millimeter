"""Publishes some data needed globally on the site"""
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def site_title():
    return settings.SITE_TITLE

