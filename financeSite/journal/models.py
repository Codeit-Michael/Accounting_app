from django.db import models

# Create your models here.

class my_journal(models.Model):
	text = models.CharField(max_length=30)

	def __str__(self):
		return self.text

class debit(models.Model):
	journal_list = models.ForeignKey(my_journal,on_delete=models.CASCADE)
	dbt = models.CharField(max_length=30)
	dbt_amount = models.IntegerField()

	def __str__(self):
		return self.dbt

class credit(models.Model):
	contra_trans = models.ForeignKey(debit, on_delete=models.CASCADE)
	cdt = models.CharField(max_length=30)
	cdt_amount = models.IntegerField()

	def __str__(self):
		return self.cdt

class transaction(models.Model):
	list = models.ForeignKey(my_journal,on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	accounts = models.CharField(max_length=30)
	amount = models.IntegerField()

	def __str__(self):
		return self.name