from django.db import models


class BankAccount(models.Model):
	debit = models.IntegerField()
	nip = models.IntegerField()
	amount = models.IntegerField(default=0)
	locked = models.BooleanField(default=False)


	def __str__(self):
		return str(self.debit)
