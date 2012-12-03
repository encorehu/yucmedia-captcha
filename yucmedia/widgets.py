# -*- coding: utf-8 -*- 
# ------------------------------------------------------------
# Script   Name: widgets.py
# Creation Date: 2011-10-28  05:42
# Last Modified: 2011-11-12 18:33:40
# Copyright (c)2011, DDTCMS Project
# Purpose: This file used for DDTCMS Project
# ------------------------------------------------------------

# python.
#
# ------------------------------------------------------------

# django.
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import RequestContext
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _
# ------------------------------------------------------------

# 3dpart.
from client import captcha

#if you want to use different captcha servers, plug them in here
#captcha.API_SERVER="http://www.google.com/recaptcha/api"
#captcha.VERIFY_SERVER="www.google.com/recaptcha/api"
# ------------------------------------------------------------


YUC_CAPCHA_ID  = 'id_yuc_capcha'

class YucmediaCaptchaInput(forms.TextInput):
    yucmedia_bmserialnum_name = 'BMserialnum'
    yucmedia_response_name    = 'recaptcha_response_field'

    class Media:
        js  = (
        #        'http://api.yucmedia.com/script/script.js?key=%s&inputid=id_yuc_capcha&offtop=0&offleft=0&zbkey=dpy' % (settings.YUCMEDIA_SITEKEY, YUC_CAPCHA_ID),
        )

    def __init__(self, attrs = {}):
    	self.attrs = {'zbkey': 'dpy','size':'10'}       
        if attrs is not None:
            self.attrs.update(attrs)
        super(YucmediaCaptchaInput, self).__init__(self.attrs)

    def render(self, name, value, attrs=None):
        rendered = super(YucmediaCaptchaInput, self).render(name, value, attrs)
        self.yucmedia_response_name=name
        use_ssl = False
        if 'RECAPTCHA_USE_SSL' in settings.__members__:
            use_ssl = settings.RECAPTCHA_USE_SSL
        return rendered+mark_safe(u'%s' %
                         captcha.displayhtml(settings.YUCMEDIA_SITEKEY, name, zbkey=self.attrs.get('zbkey',''),
                                             use_ssl=use_ssl))

    def value_from_datadict(self, data, files, name):
        self.yucmedia_response_name =name
        return [data.get(self.yucmedia_response_name, None),
                data.get(self.yucmedia_bmserialnum_name, None),
                data.get('userip', None),
                data.get('zbkey', 'dpy')]
            


