from django.db import models

# Create your models here.
class debit(models.Model):
	dbt = models.CharField(max_length=10)
	dbt_amount = models.IntegerField()

class credit(models.Model):
	contra_trans = models.ForeignKey(debit, on_delete=models.CASCADE)
	cdt = models.CharField(max_length=10)
	cdt_amount = models.IntegerField()