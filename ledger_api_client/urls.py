from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from ledger_api_client import views
from ledger_api_client import api

urlpatterns = [
        url(r'^ledger-api/payment-details$', views.PaymentDetailCheckout.as_view(), name='ledgergw-payment-details'),
        #url(r'^ledger-api/process-payment$', views.ProcessPaymentCheckout.as_view(), name='ledgergw-process-payment'),
        # api
        url(r'^ledger-api/process-payment', api.process_payment),
        url(r'^ledger-api/process-refund', api.process_refund),

]
