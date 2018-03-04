import urllib
import urllib.request
import json
#import pandas as pd
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
    pull_from_crypto = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").read().decode('utf-8')
    eth_to_usd = json.loads(pull_from_crypto)["USD"]

    last_calculator_request = Calculator.objects.last()
    last_payout_amount = PayoutAmount.objects.order_by('payout_date').last()
    eth_made = last_calculator_request.coin_num*last_payout_amount.payout_amount
    usd_made = eth_made*eth_to_usd
    return render(request, "calculator_results.html", {"eth_made": eth_made,
                                                       "coin_num": last_calculator_request.coin_num,
                                                       "payout_amount": last_payout_amount.payout_amount,
                                                       "payout_date": last_payout_amount.payout_date,
                                                       "usd_made": usd_made, })


def enter_payout(request):
    # TODO add USDETH price to payout model
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


def contact(request):
    return render(request, "contact.html", {})


#def pool_owners(request):
#    transactions = pd.read_csv("calculator/static/POOL_Transactions/POOL_Activity_2017_01_01_to_2018_02_27.csv")
#    owner_lookup = {}
#    # when people get rid of coins, this will subtract from their total
#    for i, j in enumerate(transactions.values):
#        try:
#            owner_lookup[j[4]] = owner_lookup[j[4]] + j[-1] * -1
#        except:
#            owner_lookup[j[4]] = j[-1] * -1
#    # now do the recipients of the coins
#    for i, j in enumerate(transactions.values):
#        try:
#            owner_lookup[j[5]] = owner_lookup[j[5]] + j[-1]
#        except:
#            owner_lookup[j[5]] = j[-1]
#    total_pool = 0
#    for wallet, value in owner_lookup.items():
#        if(wallet != "0x0000000000000000000000000000000000000000" and wallet != '0x009d7bde00c7b4025e4110cd73261d760a349133' ):
#            total_pool += value
#    return render(request, "pool_owners.html", {"coin_holders": owner_lookup, "total_pool": total_pool})


def historical_payouts(request):
    payout_amounts = PayoutAmount.objects.order_by('payout_date').values()
    pull_from_crypto = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD").read().decode('utf-8')
    current_eth_to_usd = json.loads(pull_from_crypto)["USD"]
    current_usd = payout_amounts.all().values()
    payout_values = []
    for i in payout_amounts:
        payout_values.append(i)
    for i, payout_value in enumerate(payout_values):
        payout_value["usd_historical_payout"] = payout_value["payout_amount"] * payout_value["historical_usd_to_eth"]
        payout_value["usd_current_payout"] = payout_value["payout_amount"] * current_eth_to_usd
    return render(request, "historical_payouts.html", {"payout_values": payout_values})
