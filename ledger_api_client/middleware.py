from django import http, VERSION
from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.db.models import signals
from django.utils.deprecation import MiddlewareMixin
import urllib.request, json
import urllib.parse
from django.contrib import messages

class SSOLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        User = get_user_model()

        if (request.path.startswith('/logout') or request.path.startswith('/ledger/logout')) \
                    and 'HTTP_X_LOGOUT_URL' in request.META and request.META['HTTP_X_LOGOUT_URL']:
            logout(request)
            return http.HttpResponseRedirect(request.META['HTTP_X_LOGOUT_URL'])

        if VERSION < (2, 0):
            user_auth = request.user.is_authenticated()
        else:
            user_auth = request.user.is_authenticated

        if not user_auth and 'HTTP_REMOTE_USER' in request.META and request.META['HTTP_REMOTE_USER']:

            attributemap = {
                'username': 'HTTP_REMOTE_USER',
                'last_name': 'HTTP_X_LAST_NAME',
                'first_name': 'HTTP_X_FIRST_NAME',
                'email': 'HTTP_X_EMAIL',
            }

            for key, value in attributemap.items():
                if value in request.META:
                    attributemap[key] = request.META[value]

            if hasattr(settings, 'ALLOWED_EMAIL_SUFFIXES') and settings.ALLOWED_EMAIL_SUFFIXES:
                allowed = settings.ALLOWED_EMAIL_SUFFIXES
                if isinstance(settings.ALLOWED_EMAIL_SUFFIXES, basestring):
                    allowed = [settings.ALLOWED_EMAIL_SUFFIXES]
                if not any([attributemap['email'].lower().endswith(x) for x in allowed]):
                    return http.HttpResponseForbidden()

            if attributemap['email'] and User.objects.filter(email__iexact=attributemap['email']).exists():
                user = User.objects.filter(email__iexact=attributemap['email'])[0]
            elif (User.__name__ != 'EmailUser') and User.objects.filter(username__iexact=attributemap['username']).exists():
                user = User.objects.filter(username__iexact=attributemap['username'])[0]
            else:
                user = User()

            # connect to ledger and align local cache account
            json_response = {}
            data = urllib.parse.urlencode(attributemap)
            data = data.encode('utf-8')
            with urllib.request.urlopen(settings.LEDGERGW_URL+"ledgergw/remote/user/"+attributemap['email']+"/"+settings.LEDGER_API_KEY+"/", data) as url:
                   json_response = json.loads(url.read().decode())

            if 'user' in json_response:
                attributemap['ledger_id'] = json_response['user']['ledgerid']
                attributemap['ledger_data'] = json_response['user']
                attributemap['is_superuser'] = json_response['user']['is_superuser']
                attributemap['is_staff'] = json_response['user']['is_staff']
                attributemap['ledger_groups'] = json_response['user']['groups']
            else:
                messages.error(request, 'Unable to Update User Information from Ledger')
            user.__dict__.update(attributemap)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
