from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.month_check, name='month_check'),
    url(r'^payout/new/$', views.enter_payout, name='enter_payout'),
    url(r'^results/', views.calculator_results, name='calculator_results'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    #url(r'^owners/', views.pool_owners, name='pool_owners'),
    url(r'^historical/', views.historical_payouts, name='historical_payout'),
]