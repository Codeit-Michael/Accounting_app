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

    return render(response,'journal/index.html',{'cnt':cnt})

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
    t_accounts = {}
    trial_balance = {}

    # yet working
    for item in cnt.debit_set.all():
        # (.first) to get the 1st item and (.last) as opposite
        newItem = item.credit_set.first()
        if item.dbt not in t_accounts:
            t_accounts[item.dbt] = {}
            t_accounts[item.dbt]['debit'] = []
            t_accounts[item.dbt]['credit'] = []
            trial_balance[item.dbt] = {}
            trial_balance[item.dbt]['debit'] = 0
            trial_balance[item.dbt]['credit'] = 0
        
        if newItem.cdt not in t_accounts:
            t_accounts[newItem.cdt] = {}
            t_accounts[newItem.cdt]['debit'] = []
            t_accounts[newItem.cdt]['credit'] = []
            trial_balance[newItem.cdt] = {}
            trial_balance[newItem.cdt]['debit'] = 0
            trial_balance[newItem.cdt]['credit'] = 0

        t_accounts[item.dbt]['debit'].append(item.dbt_amount)
        t_accounts[newItem.cdt]['credit'].append(newItem.cdt_amount)
        trial_balance[item.dbt]['debit'] += item.dbt_amount
        trial_balance[newItem.cdt]['credit'] += newItem.cdt_amount

    print(trial_balance)

    return render(response, 'journal/ledgers.html', {'t_accounts':t_accounts})

    """ FIX THE SUM OF DEBITS AND CREDIT FOR EACH TRANSACTION """