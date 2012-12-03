#coding=utf-8
from django.conf import settings
from django import forms
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from random import random
from django.utils.translation import ugettext_lazy as _

from widgets import YucmediaCaptchaInput
from fields import YucmediaCaptchaField


class YucmediaCaptchaForm(forms.Form):
    yuc_captcha   = YucmediaCaptchaField()
    userip        = forms.CharField(required=False,widget=forms.HiddenInput)
    
    
from django.contrib.comments.forms import CommentForm, CommentSecurityForm
# To customize the comment form, you can uncomment any or all of these
# lines, move them into the CommentCaptchaForm class, and edit the
# characteristics of the field you want to change. See
# django's form fields documentation
# [http://docs.djangoproject.com/en/dev/ref/forms/fields/](here)
#
# You may need some or all of these imports:
# from django.conf import settings
# from django import forms
# from django.utils.translation import ungettext, ugettext_lazy as _
#
# and the comment field requires this line at the module level:
# COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)
#
#name          = forms.CharField(label=_("Name"), max_length=50)
#email         = forms.EmailField(label=_("Email address"))
#url           = forms.URLField(label=_("URL"),
#                               required=False)
#
#comment       = forms.CharField(label=_('Comment'),
#                                widget=forms.Textarea,
#                                max_length=COMMENT_MAX_LENGTH)
COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class CaptchaCommentForm(CommentForm):
    name          = forms.CharField( required=False,widget=forms.HiddenInput)
    url           = forms.CharField( required=False,widget=forms.HiddenInput)
    email         = forms.EmailField(label=_("Email address"))
    comment       = forms.CharField(label=_('Comment'),
                                    widget=forms.Textarea,
                                    max_length=COMMENT_MAX_LENGTH)
    captcha       = YucmediaCaptchaField()
    
    def clean_name(self):
        return "noname"
    
    def clean(self):
        cleaned_data=self.cleaned_data
        username  = cleaned_data['email'].split('@')[0]
        cleaned_data['name'] = username
        # Always return the full collection of cleaned data.
        return cleaned_data


class YucmediaCaptchaCommentForm(CommentForm):
    captcha       = YucmediaCaptchaField()