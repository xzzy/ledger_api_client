from django.conf import settings
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
    print ("LOADING create_basket_session")
    print (emailuser_id)
    print (parameters)
    payment_session = None
    cookies = None 
    if 'payment_session' in request.session:
          payment_session = request.session.get('payment_session')
          cookies = {'sessionid': payment_session}
    print ("PAYMENT SESSION")
    print (payment_session)
    print (parameters)
    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-basket-session/'+api_key+'/'
    myobj = {'parameters': json.dumps(parameters), 'emailuser_id': emailuser_id}
    print (api_key)
    print (url)

    # send request to server to get file
    resp = requests.post(url, data = myobj, cookies=cookies)
    print ("COOk1")
    print (resp)
    for c in resp.cookies:
         if c.name ==  'sessionid':
             print ("CREATING PAYMENT SESSION")
             request.session['payment_session'] = c.value
             print (request.session['payment_session'])
         print(c.name, c.value)
    request.session['basket_hash'] = resp.json()['data']['basket_hash']
    return resp.json()['data']['basket_hash']

def create_checkout_session(request, checkout_parameters):

    print ("LOADING create_basket_session")
    print (checkout_parameters)

    api_key = settings.LEDGER_API_KEY
    url = settings.LEDGER_API_URL+'/ledgergw/remote/create-checkout-session/'+api_key+'/'
    myobj = {'checkout_parameters': json.dumps(checkout_parameters),}
    cookies = {}
    if 'payment_session' in request.session:
        payment_session = request.session.get('payment_session')
        cookies = {'sessionid': payment_session}
    print (api_key)
    print (url)

    print ("R S")
    session = requests.Session()
    # send request to server to get file
    resp = requests.post(url, data = myobj, cookies=cookies)
    for c in resp.cookies:
        print(c.name, c.value)

        if c.name ==  'sessionid':
             print ("CREATING PAYMENT SESSION")
             request.session['payment_session'] = c.value
             print (request.session['payment_session'])
        
    print ("RS END")
    print(session.cookies.get_dict())

    #print (resp.json()['data'])
    #return resp.json()['data']['basket_hash']


def payment_details_checkout(request):
    pass
#/ledger/checkout/checkout/payment-details/


def place_order_submission():
    pass


def use_existing_basket():
    pass

def use_existing_basket_from_invoice():
    pass



class OrderObject():
     def __init__(self):
           self.id = None
           self.number = None


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
             print (resp)            
             print (resp.text)
             o = OrderObject()
             o.id = resp.json()['data']['order']['id']
             o.number = resp.json()['data']['order']['number']

             return o 
