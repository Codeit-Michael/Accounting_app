from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
def journal_table(context, pfl):
    request = context.get('request')
    
    trans_table = []
    debit_total, credit_total = 0, 0
    for x, y in zip(pfl.debit_set.all(), pfl.credit_set.all()):
        trans_table.append((x.date, x.dbt, x.amount, ''))
        trans_table.append((y.date, y.cdt, '', y.amount))
        debit_total += x.amount
        credit_total += y.amount
    context = {'tbl': trans_table, 'dt': debit_total, 'ct': credit_total}
    return context
