from django.shortcuts import render
from django.http import HttpResponse
from .models import debit,credit

# Create your views here.

def index(response):
    jl = debit.objects
    return render(response,'journal/index.html',{'jl':jl})

# plan and make the free fill journal site