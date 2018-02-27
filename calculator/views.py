import urllib
import urllib.request
import json
#from urllib.request import urlopen
from django.shortcuts import render, redirect
from .forms import PayoutForm, CalculatorForm
from .models import PayoutAmount, Calculator


def month_check(request):
    if request.method == "POST":
        form = CalculatorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("calculator_results")
    else:
        form = CalculatorForm()
    return render(request, "home.html", {'form': form})


def calculator_results(request):
    eth_to_usd = json.loads(urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").read())["USD"]
    last_calculator_request = Calculator.objects.last()
    last_payout_amount = PayoutAmount.objects.last()
    eth_made = last_calculator_request.coin_num*last_payout_amount.payout_amount
    usd_made = eth_made*eth_to_usd

    return render(request, "calculator_results.html", {"eth_made": eth_made,
                                                       "coin_num": last_calculator_request.coin_num,
                                                       "payout_amount": last_payout_amount.payout_amount,
                                                       "payout_date": last_payout_amount.payout_date,
                                                       "usd_made": usd_made, })


def enter_payout(request):
    if request.method == "POST":
        form = PayoutForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("month_check")
    else:
        form = PayoutForm()
    return render(request, "enter_payout.html", {'form': form})


def about(request):
    return render(request, "about.html", {})
