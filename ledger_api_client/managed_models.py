from __future__ import unicode_literals

import os
import zlib

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.db import models, IntegrityError, transaction
#from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_delete, pre_save, post_save
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django_countries.fields import CountryField
#from ledger_api_client import ledger_models
from datetime import datetime, date
from django.contrib.auth.models import Permission
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from django.core.cache import cache
import json

class SystemGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description= models.TextField(blank=True, null=True, default='')
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='ledger_api_permissions',
        blank=True,
    )

    class Meta:
        verbose_name = 'System Group'
        verbose_name_plural = 'System Groups'

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def save(self, *args, **kwargs):
        cache.delete("managed_models.SystemGroup.objects.filter(id="+str(self.id)+")") 
        cache.delete("managed_models.SystemGroup.get_system_group_member_ids:"+str(self.id))
        cache.delete("managed_models.SystemGroup.objects.filter(name="+str(self.name)+")")
        cache.delete("managed_models.SystemGroup.get_system_group_member_ids_active_users:"+str(self.id))
        super(SystemGroup, self).save(*args, **kwargs)

    def get_system_group_member_ids(self):
        spg_array = []
        spg_array_cache = cache.get("managed_models.SystemGroup.get_system_group_member_ids:"+str(self.id))
        
        if spg_array_cache is None:
            spg = SystemGroupPermission.objects.filter(system_group=self)
            for p in spg:
                spg_array.append(p.emailuser.id)
            cache.set("managed_models.SystemGroup.get_system_group_member_ids:"+str(self.id), json.dumps(spg_array), 86400)
        else:
            spg_array = json.loads(spg_array_cache)
        return spg_array
    
    def get_system_group_member_ids_active_users(self):
        spg_array = []
        spg_array_cache = cache.get("managed_models.SystemGroup.get_system_group_member_ids_active_users:"+str(self.id))
        # ,emailuser__active=True
        if spg_array_cache is None:
            spg = SystemGroupPermission.objects.filter(system_group=self)
            for p in spg:
                if p.emailuser.is_active is True:
                    spg_array.append(p.emailuser.id)
                cache.set("managed_models.SystemGroup.get_system_group_member_ids_active_users:"+str(self.id), json.dumps(spg_array), 86400)
        else:
            spg_array = json.loads(spg_array_cache)
        return spg_array    


#customer = models.ForeignKey(EmailUser, on_delete=models.PROTECT, blank=True, null=True)

class SystemGroupPermission(models.Model):
      system_group = models.ForeignKey(SystemGroup, on_delete=models.PROTECT)
      emailuser = models.ForeignKey(EmailUser, on_delete=models.PROTECT, blank=True, null=True, db_constraint=False)
      active = models.BooleanField(default=True)

      def __str__(self):
            return str(self.system_group)


class SystemUser(models.Model):
    """Custom authentication model for the ledger project.
    Password and email are required. Other fields are optional.
    """
    ledger_id = models.OneToOneField(EmailUser, on_delete=models.DO_NOTHING, db_constraint=False, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, default=None)
    first_name = models.CharField(max_length=128, blank=False, verbose_name='Given name(s)')
    last_name = models.CharField(max_length=128, blank=False, verbose_name='Last name')

    legal_first_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Legal Given name(s)')
    legal_last_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Legal Last name')

    account_change_locked = models.BooleanField(
        default=False,
        help_text='Will lock the account details preventing changes to the account information.',
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into the admin site.',
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active.'
                  'Unselect this instead of deleting ledger.accounts.',
    )
    created = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr')
    )
    
    title = models.CharField(max_length=100, choices=TITLE_CHOICES, null=True, blank=True, verbose_name='title', help_text='')
    # dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False, verbose_name="date of birth", help_text='')
    legal_dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name="Legal date of birth", help_text='')
    phone_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="phone number", help_text='')  
    mobile_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="mobile number", help_text='')
    fax_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="fax number", help_text='')

    # residential_address = models.ForeignKey(Address, null=True, blank=False, related_name='+')
    # postal_address = models.ForeignKey(Address, null=True, blank=True, related_name='+')
    # postal_same_as_residential = models.NullBooleanField(default=False) 
    # billing_address = models.ForeignKey(Address, null=True, blank=True, related_name='+')
    # billing_same_as_residential = models.NullBooleanField(default=False)

    # identification = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='identification_document')
    # identification2 = models.ForeignKey(PrivateDocument, null=True, blank=True, on_delete=models.SET_NULL, related_name='identification_document_2')

    # senior_card = models.ForeignKey(Document, null=True, blank=True, on_delete=models.SET_NULL, related_name='senior_card')
    # senior_card2 = models.ForeignKey(PrivateDocument, null=True, blank=True, on_delete=models.SET_NULL, related_name='senior_card')

    # def save(self, *args, **kwargs):
    #     print (self.ledger_id.id)
    #     print (self.pk)
    #     # if self.pk is None:
    #     #     System               
    #     super(SystemUser, self).save(*args, **kwargs)
    
    # def create(self, *args, **kwargs):
    #     self.through_defaults=None
    #     print ("CREATE")
    #     super(SystemUser, self).save(*args, **kwargs)
    

    def __str__(self):
        if self.legal_first_name:                        
            return '{} {}'.format(self.legal_first_name, self.legal_last_name)
        else:
            if self.first_name:
                return '{} {}'.format(self.first_name, self.last_name)
            return '{}'.format(self.ledger_id_id)      

class SystemUserAddress(models.Model):

    STATE_CHOICES = (
        ('ACT', 'ACT'),
        ('NSW', 'NSW'),
        ('NT', 'NT'),
        ('QLD', 'QLD'),
        ('SA', 'SA'),
        ('TAS', 'TAS'),
        ('VIC', 'VIC'),
        ('WA', 'WA')
    )    
    ADDRESS_TYPE = (
            ('residential_address', 'Residential Address'),
            ('postal_address', 'Postal Address'),
            ('billing_address', 'Billing Address'),
    )

    system_user = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    address_type = models.CharField(choices=ADDRESS_TYPE, max_length=50, blank=True, null=True )
    line1 = models.CharField('Line 1', max_length=255, blank=True, null=True)
    line2 = models.CharField('Line 2', max_length=255, blank=True, null=True)
    line3 = models.CharField('Line 3', max_length=255, blank=True, null=True)
    locality = models.CharField('Suburb / Town', max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=255, default='WA', blank=True, null=True)
    country = CountryField(default='AU', blank=True, null=True)
    use_for_postal = models.BooleanField(default=False)   
    use_for_billing = models.BooleanField(default=False)
    system_address_link = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return '{} {} {} {} {}'.format(self.line1, self.locality, self.state,self.country,self.postcode)


