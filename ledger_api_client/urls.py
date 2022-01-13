from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from ledger_api_client import views
from ledger_api_client import api
from django.contrib.auth import logout, login
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.urls import path

urlpatterns = [
        url(r'^ledger-api/payment-details$', views.PaymentDetailCheckout.as_view(), name='ledgergw-payment-details'),
        #url(r'^ledger-api/process-payment$', views.ProcessPaymentCheckout.as_view(), name='ledgergw-process-payment'),
        # api
        url(r'^ledger-api/get-card-tokens', api.get_card_tokens),
        url(r'^ledger-api/delete-card-token/(?P<card_token_id>[0-9]+)/', api.delete_card_token),
        url(r'^ledger-api/process-payment', api.process_payment),
        url(r'^ledger-api/process-refund', api.process_refund),
        url(r'^ledger-api/process-zero', api.process_zero),
        url(r'^ledger-ui/accounts',  views.AccountsView.as_view(), name='ledger-api-invoice-pdf'),
        url(r'^ledger-toolkit-api/invoice-pdf/(?P<reference>\d+)',views.InvoicePDFView.as_view(), name='ledger-api-invoice-pdf'),


]
if settings.ENABLE_DJANGO_LOGIN is True:
    urlpatterns.append(url(r'^login/', LoginView.as_view(),name='login'))
urlpatterns.append(url(r'^logout/$', LogoutView.as_view(), {'next_page': '/'}, name='logout'))


#    print ("TYES")
    #urlpatterns.append(path('login/', login, name='login'),)
