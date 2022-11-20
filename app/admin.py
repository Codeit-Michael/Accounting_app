from django.contrib import admin
from .models import Portfolio, Debit, Credit

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Debit)
admin.site.register(Credit)