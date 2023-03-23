from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .models import BankAccount



class GetBankAccountsView(APIView):
	"""
	Trae todas las tarjetas de débito
	"""
	def get(self, request, format=None):
		debits = [account.debit for account in BankAccount.objects.all()]
		return Response(debits)
	
