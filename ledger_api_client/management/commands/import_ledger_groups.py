from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import timedelta
from ledger_api import models

import urllib.request, json


class Command(BaseCommand):
    help = 'Import ledger groups.'

    def handle(self, *args, **options):
        print ("IMPORT LEDGER GROUP")
        json_response = {}
        with urllib.request.urlopen("https://ledgergw.digitalreach.com.au/ledgergw/remote/groups/"+settings.LEDGER_API_KEY+"/") as url:
             json_response = json.loads(url.read().decode())


        print (json_response)
        if models.DataStore.objects.filter(key_name='ledger_groups').count():
            models.DataStore.objects.filter(key_name='ledger_groups').update(data=json_response)
        else:
            models.DataStore.objects.create(key_name='ledger_groups', data=json_response)

