from django import template
from django.conf import settings
from yucmedia.client import captcha

register = template.Library()

@register.simple_tag
def yucmediacaptcha_html():
    return captcha.displayhtml(settings.YUCMEDIA_SITEKEY)
