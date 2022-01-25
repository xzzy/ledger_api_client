from __future__ import unicode_literals

import os
import zlib

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import JSONField
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

class SystemGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
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
        super(SystemGroup, self).save(*args, **kwargs)


#customer = models.ForeignKey(EmailUser, on_delete=models.PROTECT, blank=True, null=True)

class SystemGroupPermission(models.Model):
      system_group = models.ForeignKey(SystemGroup, on_delete=models.PROTECT)
      emailuser = models.ForeignKey(EmailUser, on_delete=models.PROTECT, blank=True, null=True, db_constraint=False)
      active = models.BooleanField(default=True)

      def __str__(self):
            return str(self.system_group)

