from django.urls import path
from . import views

app_name = 'journal'
urlpatterns = [
    path('',views.home,name='home'),
    path('<int:id>',views.index,name='index'),
    path('create/',views.create,name='create'),
    path('<int:id>/ledger/',views.ledger,name='ledger'),
    path('<int:id>/trialbalance/',views.trial_balance,name='trial_balance'),
]