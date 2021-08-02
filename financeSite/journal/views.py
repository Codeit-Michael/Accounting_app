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
                db = cnt.debit_set.create(dbt=dtext,dbt_amount=int(amt))
                cd = db.credit_set.create(cdt=ctext,cdt_amount=int(amt))
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

