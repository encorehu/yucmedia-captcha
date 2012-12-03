import urllib2, urllib

API_SSL_SERVER  = "https://api.yucmedia.com"
API_SERVER      = "http://api.yucmedia.com"
VERIFY_SERVER   = "api.yucmedia.com"

class YucmediaCaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (sitekey, inputid='yuc_capcha', zbkey='dpy',
                 use_ssl = False,
                 error = None):
    """Gets the HTML to display for YucmediaCaptcha

    sitekey -- The sitekey api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from YucmediaCaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<script src="%(ApiServer)s/script/script.js?key=%(sitekey)s&inputid=id_%(inputid)s&offtop=0&offleft=0&zbkey=%(zbkey)s"></script>
<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(sitekey)s&inputid=id_%(inputid)s&offtop=0&offleft=0&zbkey=%(zbkey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="yucmedia_bmserialnum_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='yucmedia_response_field' value='manual_challenge' />
</noscript>
""" % {
        'ApiServer' : server,
        'sitekey' : sitekey,
        'inputid' : inputid,
        'zbkey' : zbkey,
        'ErrorParam' : error_param,
        }


def submit (yucmedia_bmserialnum_field,
            yucmedia_response_field,
            remoteip,
            zbkey,
            sitekey,
            idenkey
            ):
    """
    Submits a YucmediaCaptcha request for verification. Returns YucmediaCaptchaResponse
    for the request

    yucmedia_bmserialnum_field -- The value of yucmedia_bmserialnum_field from the form
    yucmedia_response_field --    The value of yucmedia_response_field from the form
    sitekey,
            idenkey, -- your reCAPTCHA private key
    remoteip -- the user's ip address
    
    """
    if not (yucmedia_response_field and yucmedia_bmserialnum_field and
            len (yucmedia_response_field) and len (yucmedia_bmserialnum_field)):
        return YucmediaCaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'sitekey':      encode_if_necessary(sitekey),
            'serialnum':    encode_if_necessary(yucmedia_bmserialnum_field),
            'userip':       encode_if_necessary(remoteip),
            'userresponse': encode_if_necessary(yucmedia_response_field),
            'idenkey':      encode_if_necessary(idenkey), 
            'zbkey':        encode_if_necessary(zbkey),
            })

    request = urllib2.Request (
        url = 'http://%s/script/verify' % VERIFY_SERVER ,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'Host':         VERIFY_SERVER,
            "User-agent": "yucmedia/python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read().splitlines();
    httpresp.close();

    return_code = return_values[0][0:4]
            
    if (return_code == "true"):
        return YucmediaCaptchaResponse(is_valid=True)
    else:
        return YucmediaCaptchaResponse(is_valid=False, error_code = return_values [0])