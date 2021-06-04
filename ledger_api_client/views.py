import logging
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms
from datetime import datetime, timedelta
#from django.template import Template, Context,RequestContext
#from django.template import loader
from django.template.loader import render_to_string
from decimal import *
import requests

class PaymentDetailCheckout(TemplateView):
    template_name = 'payments/payment-details.html'

    def get(self, request, *args, **kwargs):
        # if page is called with ratis_id, inject the ground_id
        context = {}
        cookies = {}
        api_key = settings.LEDGER_API_KEY
        url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/payment-details/'
        payment_session = None
        basket_hash = ""

        if 'payment_session' in request.session:
              payment_session = request.session.get('payment_session')
              basket_hash = request.session.get('basket_hash')
              cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true','LEDGER_API_KEY': api_key}

        myobj = {'payment_method':'card',}

        # send request to server to get file
        # allow_redirects=False
        try: 
             resp = requests.get(url, data = myobj, cookies=cookies)
             context['data'] = resp.text
        except Exception as e:
             context['data'] = render_to_string('payments/gateway-error.html', {'error': 'There was an error connecting to the Payment Gateway please try again later',},)             
             #context['data'] = "There was error connecting to the Payment Gateway please try again later"
        return render(request, self.template_name, context)

#class ProcessPaymentCheckout(TemplateView):
#    template_name = 'payments/payment-details.html'
#
#    def get(self, request, *args, **kwargs):
#        # if page is called with ratis_id, inject the ground_id
#        # /ledger/checkout/checkout/payment-details/
#
#        context = {}
#        cookies = {}
#        api_key = settings.LEDGER_API_KEY
#        url = settings.LEDGER_API_URL+'/ledger/checkout/checkout/payment-details/'
#        payment_session = None
#        basket_hash = ""
#
#        if 'payment_session' in request.session:
#              payment_session = request.session.get('payment_session')
#              basket_hash = request.session.get('basket_hash')
#              print ("BASKET HASH")
#              print (basket_hash)
#              cookies = {'sessionid': payment_session, 'ledgergw_basket': basket_hash, 'no_header': 'true', 'payment_api_wrapper': 'true', 'LEDGER_API_KEY': api_key}
#
#        print ("PAYMENT SESSION")
#        print (payment_session)
#        myobj = {}
#
#        # send request to server to get file
#        # allow_redirects=False
#        resp = requests.get(url, data = myobj, cookies=cookies)
#        context['data'] = resp.text
#        print (resp.headers)
#
#        #print (resp.text)
#
#
#        return render(request, self.template_name, context)
#
