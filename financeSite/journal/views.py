from django.db.models.manager import EmptyManager
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import my_journal,debit,credit
from .forms import createjournal

# Create your views here.

def home(response):
    jl = my_journal.objects
    return render(response,'journal/home.html',{'jl':jl})

def index(response,id):
    cnt = my_journal.objects.get(id=id)

    left,right = 0,0

    if response.method == 'POST':
        dtext = response.POST.get('debitTrans')
        ctext = response.POST.get('creditTrans')
        amt = response.POST.get('amount')

        try:
            if len(dtext) > 0 and int(amt) > 0 and len(ctext) > 0:
                db = cnt.debit_set.create(dbt=dtext,dbt_amount=amt)
                cd = db.credit_set.create(cdt=ctext,cdt_amount=amt)
                db.save()
                cd.save()
            else:
                return render(response,'journal/index.html',{'cnt':cnt})
        except:
            return render(response,'journal/index.html',{'cnt':cnt})

    for x in cnt.debit_set.all():
        left += x.dbt_amount
        for y in x.credit_set.all():
            right += y.cdt_amount

    return render(response,'journal/index.html',{'cnt':cnt,'left':left,'right':right})

def create(response):
    if response.method == 'POST':
        form = createjournal(response.POST)
        if form.is_valid():
            new_jl = form.cleaned_data['journal_name']
            new_trans = my_journal(text=new_jl)
            new_trans.save()
        return HttpResponseRedirect('/')
    else:
        form = createjournal()
    return render(response,'journal/create.html',{'form':form})

def ledger(response,id):
    cnt = my_journal.objects.get(id=id)
    trans = cnt.transaction_set
    t_accounts = {}
    trial_balance = {}

    for item in cnt.debit_set.all():
        # (.first) to get the 1st item and (.last) as opposite
        newItem = item.credit_set.first()
        if item.dbt not in t_accounts:
            t_accounts[item.dbt] = {}
            t_accounts[item.dbt]['debit'] = [0]
            t_accounts[item.dbt]['credit'] = [0]
        
        if newItem.cdt not in t_accounts:
            t_accounts[newItem.cdt] = {}
            t_accounts[newItem.cdt]['debit'] = [0]
            t_accounts[newItem.cdt]['credit'] = [0]

        t_accounts[item.dbt]['debit'].append(item.dbt_amount)
        t_accounts[newItem.cdt]['credit'].append(newItem.cdt_amount)
        t_accounts[item.dbt]['debit'][0] += item.dbt_amount
        t_accounts[newItem.cdt]['credit'][0] += newItem.cdt_amount

    for transaction in t_accounts:
        trial_balance[f'{transaction}'] = {}
        if t_accounts[transaction]['debit'][0] > t_accounts[transaction]['credit'][0]:
            amount = t_accounts[transaction]['debit'][0] - t_accounts[transaction]['credit'][0]
            trial_balance[f'{transaction}']['debit'] = amount
        else:
            amount = t_accounts[transaction]['credit'][0] - t_accounts[transaction]['debit'][0]
            trial_balance[f'{transaction}']['credit'] = amount

    for entry in trial_balance:
        for account in trial_balance[entry]:
            if not trans.filter(name=entry):
                new = trans.create(name=entry,accounts=account,amount=trial_balance[entry][account])
                new.save()
            trans.filter(name=entry).update(name=entry,accounts=account,amount=trial_balance[entry][account])

    return render(response, 'journal/ledger.html', {'cnt':cnt,'t_accounts':t_accounts,'tb':trial_balance,})

def trial_balance(response,id):
    cnt  = my_journal.objects.get(id=id)
    tb = cnt.transaction_set
    left,right = 0,0

    for item in tb.all():
        if item.accounts == 'debit':
            left += item.amount
        else:
            right += item.amount

    print(left,right)

    return render(response,'journal/trialBalance.html',{'cnt':cnt,'tb':tb,'left':left,'right':right})
