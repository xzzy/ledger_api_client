from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta, date, datetime
from decimal import Decimal as D
from ledger_api_client import utils as utils_ledger_api_client
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from decimal import Decimal
import itertools

class Command(BaseCommand):
    help = 'Create a future invoice'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print ("RUNNING")
        lines = []
        lines.append({
             'ledger_description': 'Subscription to Camping Magazine',
             "quantity": 1,
             "price_incl_tax": '33',
             "oracle_code": 'NNP346 GST',
             "line_status" : 1
             })

        booking_id = '12121'
        old_booking_id = '13333'
        invoice_text = "Future booking for campsite booking 14"
        request =  utils_ledger_api_client.FakeRequestSessionObj()

        request.user = EmailUser.objects.get(id=2)
        customer_id = request.user.id

        basket_params = {
            'products': lines,
            'vouchers': [],
            'system': settings.PS_PAYMENT_SYSTEM_ID,
            'custom_basket': True,
            'booking_reference': 'PB-'+str(booking_id),
            'booking_reference_link': str(old_booking_id),
            'no_payment': True,
            'organisation': 7,
        }
        basket_user_id = customer_id
        basket_hash = utils_ledger_api_client.create_basket_session(request,basket_user_id, basket_params)
        
        #checkouthash =  hashlib.sha256('TEST'.encode('utf-8')).hexdigest()
        #checkouthash = request.session.get('checkouthash','')
        #basket, basket_hash = use_existing_basket_from_invoice('00193349270')
        # notification url for when payment is received.
        return_preload_url = settings.PARKSTAY_EXTERNAL_URL+'/api/complete_booking/9819873279821398732198737981298/'+str(booking_id)+'/'
        basket_hash_split = basket_hash.split("|")
        pcfi = utils_ledger_api_client.process_create_future_invoice(basket_hash_split[0], invoice_text, return_preload_url)
        print (pcfi)


