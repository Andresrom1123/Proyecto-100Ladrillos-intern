from django.db import models


class BankAccount(models.Model):
	debit = models.CharField(max_length=16)
	nip = models.CharField(max_length=16)
	amount = models.IntegerField(default=0)
	withdraw = models.IntegerField(default=0)
	locked = models.BooleanField(default=False)


	def __str__(self):
		return str(self.debit)
