from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import timedelta
from ledger_api_client import models

import urllib.request, json


class Command(BaseCommand):
    help = 'Import ledger groups.'

    def handle(self, *args, **options):
        print ("Using ledgergw "+settings.LEDGERGW_URL+" to determine IP address")
        json_response = {}
        with urllib.request.urlopen(settings.LEDGERGW_URL+"ledgergw/ip-check/") as url:
             json_response = json.loads(url.read().decode())
        print (json_response)

