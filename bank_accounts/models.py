from django.db import models


class BankAccount(models.Model):
	debit = models.CharField(max_length=16)
	nip = models.CharField(max_length=16)
	amount = models.IntegerField(default=0)
	locked = models.BooleanField(default=False)
	nip_incorrect = models.IntegerField(default=0)

	def __str__(self):
		return str(self.debit)
