from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import threading
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from datetime import datetime
import json
import time
import hashlib
from datetime import timedelta
from ledger_api_client import utils as utils_ledger_api_client

class Command(BaseCommand):
    help = 'Example script to send an automatic payment request to ledger for accounts with stored payment tokens.'

    def handle(self, *args, **options):
        try:

            #  Get ledger payment token id
            primary_card_resp = utils_ledger_api_client.get_primary_card_token_for_user(1)
            ledger_payment_token_id = primary_card_resp["primary_card"] 

            
            # Create a fake request session Id 
            request =  utils_ledger_api_client.FakeRequestSessionObj()

            # using email user assign the email user object to the fake request
            request.user = EmailUser.objects.get(id=1)

            # Payment Basket Lines
            lines = []
            lines.append({
                'ledger_description': 'Test Item 2',
                'quantity': 1,
                'price_incl_tax': '10.00',
                'oracle_code': 'NNP343 GST', 
            })

            no_payment = False
            booking_reference = "YH0001" # booking reference to assign to order
            basket_params = {
                'products': lines,
                'vouchers': [],
                'system': settings.PS_PAYMENT_SYSTEM_ID,
                'custom_basket': True,
                'booking_reference': 'PB-82828',
                'booking_reference_link': '',
                'no_payment': no_payment
            }
            
            #basket, basket_hash = create_basket_session(request, basket_params)
            basket_user_id = request.user.id  # email user id for the customer
            basket_hash = utils_ledger_api_client.create_basket_session(request,basket_user_id, basket_params)
            checkouthash =  hashlib.sha256('TEST'.encode('utf-8')).hexdigest()

            booking_hash = '3421sdafdsahasjdhkkjhdsaf' # unique random hash from your booking/appplication for completing booking
            # fallback_url,  return_url,  return_preload_url all need to be set as we are utilising the same funcationality as the payment checkout screen
            # sett all 3 values to the same.   return_preload_url is what send a completion ping back to the your application.
            checkout_params = {
                'system': settings.PS_PAYMENT_SYSTEM_ID,
                'fallback_url': settings.PARKSTAY_EXTERNAL_URL+'/api/complete_booking/'+booking_hash+'/', 
                'return_url': settings.PARKSTAY_EXTERNAL_URL+'/api/complete_booking/'+booking_hash+'/',
                'return_preload_url': settings.PARKSTAY_EXTERNAL_URL+'/api/complete_booking/'+booking_hash+'/',
                'force_redirect': True,
                'proxy': False,
                'invoice_text': "Parkstay test booking",
                'session_type' : 'ledger_api',
                'basket_owner' : basket_user_id,
                'response_type' : 'json'
            }

            utils_ledger_api_client.create_checkout_session(request,checkout_params)

            # START - Send Automatic Payment Request to Ledger
            # look at post info on payment screen an reuse
            resp = utils_ledger_api_client.process_payment_with_token(request, ledger_payment_token_id)
            print (resp)
            #END - Sent Automatic Payment Request to Ledger



        except Exception as e:
            print (e)
            #Send fail email
   


