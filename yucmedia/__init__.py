from django.core import urlresolvers
from django.contrib.comments.models import Comment
from forms import YucmediaCaptchaCommentForm,CaptchaCommentForm

#Override the default django form with our YucmediaCaptchaCommentForm. See 
#the [django documentation](http://docs.djangoproject.com/en/dev/ref/contrib/comments/custom/)
#for more details
def get_form():
    return CaptchaCommentForm #YucmediaCaptchaCommentForm
