from django import template
from app.models import Debit, Credit


register = template.Library()
@register.simple_tag()
def total_counter():
    debit_total, credit_total = 0, 0
    for x, y in zip(Debit.objects.all(), Credit.objects.all()):
        debit_total += x.amount
        credit_total += y.amount
    return debit_total, credit_total
