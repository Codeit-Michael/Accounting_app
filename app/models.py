from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Portfolio(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name

class Debit(models.Model):
	journal_list = models.ForeignKey(Portfolio,on_delete=models.CASCADE)
	dbt = models.CharField(max_length=30)
	amount = models.IntegerField()
	date = models.DateField(null=True)

	def __str__(self):
		return self.dbt

class Credit(models.Model):
	contra_trans = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
	cdt = models.CharField(max_length=30)
	amount = models.IntegerField()
	date = models.DateField(null=True)

	def __str__(self):
		return self.cdt

