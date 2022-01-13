from django.core.exceptions import ValidationError
from django.conf import settings
from decimal import Decimal
import django
import requests
import json 

def oracle_parser(): 
    pass

def update_payments():
    pass

def create_basket_session(request, emailuser_id, parameters):
    # emailuser_id use to be request vairable.  This has been 
    # replaced with the user objects.  You will need to change 
    #request to request.user.id for this function
    payment_session = None
    cookies = None 
 
    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          cookies = {'sessionid': payment_session}

    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-basket-session/'+api_key+'/'
    myobj = {'parameters': json.dumps(parameters), 'emailuser_id': emailuser_id,}

    try:
        # send request to server to get file
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
         raise ValidationError('Error: Unable to create basket session - unable to connect to payment gateway')       
    if int(resp.json()['status']) == 200:
         for c in resp.cookies:
              if c.name ==  'sessionid':
                  request.session['payment_session'] = c.value
         request.session['basket_hash'] = resp.json()['data']['basket_hash']
         return resp.json()['data']['basket_hash']
    else:
        raise ValidationError('Error: Unable to create basket session ') 

def create_checkout_session(request, checkout_parameters):

    django_version = float(str(django.VERSION[0])+'.'+str(django.VERSION[1]))

    checkout_parameters['user_logged_in'] = None
    is_authen = False
    if django_version > 1.11:
          is_authen = request.user.is_authenticated
    else: 
          is_authen = request.user.is_authenticated()
    if is_authen:
           checkout_parameters['user_logged_in'] = request.user.id
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-checkout-session/'+api_key+'/'
    myobj = {'checkout_parameters': json.dumps(checkout_parameters),}

    if 'basket_owner' in checkout_parameters:
        pass
    else:
        raise ValidationError('Error: "basket_owner" does not exist in create_checkout_session, this must have matching email user id')
          


    cookies = {}
    if 'payment_session' in request.session:
        payment_session = request.session.get('payment_session')
        cookies = {'sessionid': payment_session}
    session = requests.Session()
    try:
        # send request to server to get file
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
         raise ValidationError('Error: Unable to create basket session - unable to connect to payment gateway')


    if int(resp.json()['status']) == 200:
        for c in resp.cookies:
            if c.name ==  'sessionid':
                 request.session['payment_session'] = c.value
    else:
        raise ValidationError('Error: Unable to create checkout session')    

def process_api_refund(request, basket_parameters, customer_id, return_url, return_preload_url):
    django_version = float(str(django.VERSION[0])+'.'+str(django.VERSION[1]))
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/process-api-refund/'+api_key+'/'
    cookies = {}

    user_logged_in = None
    if django_version > 1.11:
          is_authen = request.user.is_authenticated
    else:
          is_authen = request.user.is_authenticated()
    if is_authen:
          user_logged_in = request.user.id

    myobj = {'basket_parameters': json.dumps(basket_parameters),'customer_id': customer_id, 'return_url': return_url, 'return_preload_url': return_preload_url, 'user_logged_in': user_logged_in}

    try:
        # send request to server to get file
        resp = requests.post(url, data = myobj, cookies=cookies)
    except Exception as e:
         raise ValidationError('Error: trying to process refund.')
    if int(resp.json()['status']) == 200:
        try:
           return resp.json()
        except Exception as e:
           print ("exception on url")
           print (e)
           return {"status": 501, "message": "error processing refund"}
    else:
        raise ValidationError('Error: Unable to create checkout session ')



def payment_details_checkout(request):
    pass
#/ledger/checkout/checkout/payment-details/


def place_order_submission():
    pass


def use_existing_basket():
    pass

def use_existing_basket_from_invoice():
    pass

def get_invoice_properties(invoice_id):
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/get-invoice/'+api_key+'/'
    myobj = {'data': json.dumps({'invoice_id': invoice_id})}
    cookies = {}
    resp = requests.post(url, data = myobj, cookies=cookies)
    resp_json = {}
    try:
        resp_json = resp.json()
        print (resp_json)
    except:
        resp_json = {}
    #print (resp.text)
    return resp_json 

def get_basket_total(basket_id):
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/get-basket-total/'+api_key+'/'
    myobj = {'data': json.dumps({'basket_id': basket_id})}
    cookies = {}
    resp = requests.post(url, data = myobj, cookies=cookies)
    resp_json = {}
    try:
        resp_json = resp.json()
    except:
        resp_json = {}
    return resp_json




class OrderObject():
     def __init__(self):
           self.id = None
           self.number = None
           self.user_id = None
           

class Order:
     class objects:
         def get(**kwargs):
             api_key = settings.LEDGER_API_KEY
             url = settings.LEDGER_API_URL+'/ledgergw/remote/get_order_info/'+api_key+'/'
             myobj = {'data': json.dumps(kwargs)}
             cookies = {}
             session = requests.Session()
             # send request to server to get file
             resp = requests.post(url, data = myobj, cookies=cookies)
             o = OrderObject()
             o.id = resp.json()['data']['order']['id']
             o.number = resp.json()['data']['order']['number']
             o.user_id = resp.json()['data']['order']['user_id']
             
             return o 

class OrderLineObject():
    def __init__(self):
        self.id = None
        self.title = None
        self.oracle_code = None
        self.quantity = None
        self.price_incl_tax = None
        self.price_excl_tax = None
        self.paid = None
        self.unit_price_incl_tax = None
        self.unit_price_excl_tax = None

class OrderLine:
      class objects:
          def filter(**kwargs):
               api_key = settings.LEDGER_API_KEY
               url = settings.LEDGER_API_URL+'/ledgergw/remote/get_order_lines/'+api_key+'/'
               myobj = {'data': json.dumps(kwargs)}
               cookies = {}
               orderlines_array = []
               session = requests.Session()
               resp = requests.post(url, data = myobj, cookies=cookies)
               for ol_e in resp.json()['data']['orderlines']:
                  ol = OrderLineObject()
                  ol.id = ol_e['id']
                  ol.title = ol_e['title']
                  ol.oracle_code = ol_e['oracle_code']
                  ol.quantity = ol_e['quantity']
                  ol.price_incl_tax = Decimal(ol_e['price_incl_tax'])
                  ol.price_excl_tax = Decimal(ol_e['price_excl_tax'])
                  ol.unit_price_incl_tax = Decimal(ol_e['unit_price_incl_tax'])
                  ol.unit_price_excl_tax = Decimal(ol_e['unit_price_excl_tax'])
                  ol.paid = Decimal(ol_e['paid'])
                  orderlines_array.append(ol)
               return orderlines_array





