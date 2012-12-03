"""
A custom Model Field for Yucmedia.
"""
from django.conf import settings
from django import forms
from django.db.models.fields import CharField
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

# We use the [recaptcha-client](http://pypi.python.org/pypi/recaptcha-client) to handle our recaptcha code
# use like above.
from client import captcha

from widgets import YucmediaCaptchaInput

class YucmediaCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Invalid captcha')
    }
    
    def __init__(self, *args, **kwargs):
        #set this field's widget to the one defined in [[widgets.py]]
        self.widget = YucmediaCaptchaInput
        self.required = True
        self.is_recaptcha = True
        super(YucmediaCaptchaField, self).__init__(*args, **kwargs)

    def validate(self, value):
        "Check if value consists only of valid captcha."

        # Use the parent's handling of required fields, etc.
        super(YucmediaCaptchaField, self).validate(value)
    
    def clean(self, values):
        #print values
        super(YucmediaCaptchaField, self).clean(values[0])
        yucmedia_response_value    = smart_unicode(values[0])
        yucmedia_bmserialnum_value = smart_unicode(values[1])
        userip   = smart_unicode(values[2])
        zbkey    = smart_unicode(values[3])
        
        check_captcha = captcha.submit( yucmedia_bmserialnum_value,
                                        yucmedia_response_value,
                                        userip,
                                        zbkey,
                                        settings.YUCMEDIA_SITEKEY, 
                                        settings.YUCMEDIA_IDENKEY)
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(check_captcha.error_code)
        return values[0]

#if 'south' in settings.INSTALLED_APPS:
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^captcha\.yucmedia\.fields\.YucmediaCaptchaField"])