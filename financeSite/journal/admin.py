from django.contrib import admin
from .models import my_journal,debit,credit, transaction

# Register your models here.
admin.site.register(my_journal)
admin.site.register(debit)
admin.site.register(credit)
admin.site.register(transaction)