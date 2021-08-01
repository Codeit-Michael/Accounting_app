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
        if response.POST.get('debit'):
            txt = response.POST.get('transaction')
            amt = response.POST.get('amount')
            if len(txt) > 2 and int(amt) > 0:
                cnt.debit_set.create(dbt=txt,dbt_amount=int(amt))
    # RECONSTRUCT!!!
    #     elif response.POST.get('credit'):
    #         txt = response.POST.get('transaction')
    #         amt = response.POST.get('amount')
    #         if len(txt) > 2 and int(amt) > 0:
    #             cnt.credit_set.create(cdt=txt,cdt_amount=int(amt))
 
    # return render(response,'journal/index.html',{'cnt':cnt})

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

