from django.db import models


class PayoutAmount(models.Model):
    payout_date = models.DateTimeField()
    payout_amount = models.FloatField()

    def new_payout(self, payout_date, payout_amount):
        self.payout_date = payout_date
        self.payout_amount = payout_amount
        self.save()


class Calculator(models.Model):
    coin_num = models.IntegerField()
