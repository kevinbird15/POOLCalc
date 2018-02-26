from django import forms

from .models import PayoutAmount, Calculator


class PayoutForm(forms.ModelForm):

    class Meta:
        model = PayoutAmount
        fields = ('payout_date', 'payout_amount')


class CalculatorForm(forms.ModelForm):

    class Meta:
        model = Calculator
        fields = ('coin_num',)
