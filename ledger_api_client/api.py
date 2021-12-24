from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from django.template.loader import render_to_string
from ledger_api_client import utils as ledger_api_client_utils
import json
import requests 
import django

@csrf_exempt
#@api_view(['POST'])
def process_payment(request):

    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}

    context = {}
    cookies = {}
    #url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/preview/'
    url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/payment-details/'
    project_code = settings.PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE
    system_id = settings.PAYMENT_INTERFACE_SYSTEM_ID
    api_key = settings.LEDGER_API_KEY
    payment_session = None
    basket_hash = ""

    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          basket_hash = request.session.get('basket_hash')
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key,}

    myobj = {'payment_method':'card','PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE': project_code,'PAYMENT_INTERFACE_SYSTEM_ID': system_id}
    for post_field in request.POST:
        if post_field == 'payment-csrfmiddlewaretoken':
             myobj['csrfmiddlewaretoken'] = request.POST[post_field]
        else:
            myobj[post_field] = request.POST[post_field]

    resp = ""
    try:
        # Set payment method first to card
        resp = requests.post(url, data = myobj, cookies=cookies)
        # now process payment
        myobj['action'] = 'place_order'
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
        resp = "ERROR Attempting to connect payment gateway please try again later"
    return HttpResponse(resp, content_type='plain/html')
    #return HttpResponse(json.dumps(jsondata), content_type='application/json')

@csrf_exempt
def process_refund(request):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    context = {}
    cookies = {}
    api_key = settings.LEDGER_API_KEY
    #url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/preview/'
    url = settings.LEDGER_API_URL+'/ledgergw/remote/process_refund/'+api_key+'/'
    project_code = settings.PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE
    system_id = settings.PAYMENT_INTERFACE_SYSTEM_ID
    api_key = settings.LEDGER_API_KEY
    payment_session = None
    basket_hash = ""

    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          basket_hash = request.session.get('basket_hash')
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key,}

    myobj = {'payment_method':'card','PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE': project_code,'PAYMENT_INTERFACE_SYSTEM_ID': system_id,}
    for post_field in request.POST:
        if post_field == 'payment-csrfmiddlewaretoken':
             myobj['csrfmiddlewaretoken'] = request.POST[post_field]
        else:
            myobj[post_field] = request.POST[post_field]

    resp = ""
    try:
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
        resp = "ERROR Attempting to connect payment gateway please try again later"
    return HttpResponse(resp, content_type='application/json')

@csrf_exempt
def process_zero(request):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    context = {}
    cookies = {}
    api_key = settings.LEDGER_API_KEY
    #url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/preview/'
    url = settings.LEDGER_API_URL+'/ledgergw/remote/process_zero/'+api_key+'/'
    project_code = settings.PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE
    system_id = settings.PAYMENT_INTERFACE_SYSTEM_ID
    api_key = settings.LEDGER_API_KEY
    payment_session = None
    basket_hash = ""

    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          basket_hash = request.session.get('basket_hash')
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key,}

    myobj = {'payment_method':'card','PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE': project_code,'PAYMENT_INTERFACE_SYSTEM_ID': system_id,} 
    for post_field in request.POST:
        if post_field == 'payment-csrfmiddlewaretoken':
             myobj['csrfmiddlewaretoken'] = request.POST[post_field]
        else:
            myobj[post_field] = request.POST[post_field]

    resp = ""
    try:
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
        resp = "ERROR Attempting to connect payment gateway please try again later"
    return HttpResponse(resp, content_type='application/json')


@csrf_exempt
def get_card_tokens(request):
    django_version = float(str(django.VERSION[0])+'.'+str(django.VERSION[1]))
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    context = {}
    cookies = {}
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/get-card-tokens/'+api_key+'/'
    project_code = settings.PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE
    system_id = settings.PAYMENT_INTERFACE_SYSTEM_ID
    api_key = settings.LEDGER_API_KEY
    payment_session = None
    basket_hash = ""

    user_logged_in = None
    if django_version > 1.11:
          is_authen = request.user.is_authenticated
    else: 
          is_authen = request.user.is_authenticated()

    if is_authen:
           user_logged_in = request.user.id

    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          basket_hash = request.session.get('basket_hash')
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key,}

    myobj = {'payment_method':'card','PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE': project_code,'PAYMENT_INTERFACE_SYSTEM_ID': system_id, 'user_logged_in' : user_logged_in}
    for post_field in request.POST:
        if post_field == 'payment-csrfmiddlewaretoken':
            myobj['csrfmiddlewaretoken'] = request.POST[post_field]
        else:
            myobj[post_field] = request.POST[post_field]

    resp = ""
    try:
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
        resp = "ERROR Attempting to connect payment gateway please try again later"
    return HttpResponse(resp, content_type='application/json')


@csrf_exempt
def delete_card_token(request, card_token_id):
    django_version = float(str(django.VERSION[0])+'.'+str(django.VERSION[1]))
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    context = {}
    cookies = {}
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/delete-card-token/'+api_key+'/'
    project_code = settings.PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE
    system_id = settings.PAYMENT_INTERFACE_SYSTEM_ID
    api_key = settings.LEDGER_API_KEY
    payment_session = None
    basket_hash = ""

    user_logged_in = None
    if django_version > 1.11:
          is_authen = request.user.is_authenticated
    else: 
          is_authen = request.user.is_authenticated()

    if is_authen:
           user_logged_in = request.user.id

    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          basket_hash = request.session.get('basket_hash')
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key,}

    myobj = {'payment_method':'card','PAYMENT_INTERFACE_SYSTEM_PROJECT_CODE': project_code,'PAYMENT_INTERFACE_SYSTEM_ID': system_id, 'card_token_id': card_token_id, 'user_logged_in' : user_logged_in}
    for post_field in request.POST:
        if post_field == 'payment-csrfmiddlewaretoken':
            myobj['csrfmiddlewaretoken'] = request.POST[post_field]
        else:
            myobj[post_field] = request.POST[post_field]

    resp = ""
    try:
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
        resp = "ERROR Attempting to connect payment gateway please try again later"
    return HttpResponse(resp, content_type='application/json')

