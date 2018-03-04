from django.db import models
import urllib.request
import json


class PayoutAmount(models.Model):
    payout_date = models.DateTimeField()
    payout_amount = models.FloatField()
    historical_usd_to_eth = models.FloatField()

    def new_payout(self, payout_date, payout_amount, historical_usd_to_eth):
        self.payout_date = payout_date
        self.payout_amount = payout_amount
        self.historical_usd_to_eth = historical_usd_to_eth
        self.save()


class Calculator(models.Model):
    coin_num = models.IntegerField()


#class WalletAccountPayout(models.Model):
#    wallet_address = models.TextField
#    payout_date = models.DateTimeField()
#    payout_amount = models.FloatField()
#    pool_qty = models.FloatField()
#    usd_eth_price = models.FloatField()
#
#    def wallet_payout(self, wallet_address, payout_date, payout_amount, pool_qty, usd_eth_price):
#        self.wallet_address = wallet_address
#        self.payout_date = payout_date
#        self.payout_amount = payout_amount
#        self.pool_qty = pool_qty
#        self.usd_eth_price = usd_eth_price
#        self.save()
