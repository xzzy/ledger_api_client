from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from django.template.loader import render_to_string
import json
import requests 

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
          cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','csrftoken': request.POST['payment-csrfmiddlewaretoken'],'LEDGER_API_KEY': api_key}

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

