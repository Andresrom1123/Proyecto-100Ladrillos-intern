from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import BankAccount


# Login
class LoginBankAccountsView(APIView):
	"""
	Mira si la tarjeta y el nip existen
	"""
	def get_object(self, debit):
		try:
			return BankAccount.objects.get(debit=debit)
		except BankAccount.DoesNotExist:
			return []
			

	def post(self, request, format=None):
		debit = request.data.get('debit')
		nip = request.data.get('nip')

		account = self.get_object(debit)

		if not account:
			return Response({'error': 'La tarjeta de débito no existe'}, status=status.HTTP_400_BAD_REQUEST)
		if account.locked:
			return Response({'error': 'La cuenta ha sido bloqueada por favor intenta con otra'}, status=status.HTTP_400_BAD_REQUEST)
		if account.nip != nip:
			return Response({'error': 'El nip es incorrecto'}, status=status.HTTP_400_BAD_REQUEST)

		return Response(status=status.HTTP_200_OK)
			
class LockedBankAccountsView(APIView):
	"""
	Bloquea una tarjeta
	"""
	def post(self, request, account_id, format=None):
		account = get_object_or_404(BankAccount.objects.all(), pk=account_id)
		account.locked = True
		account.save()
		return Response({'success': 'La cuenta ha sido bloqueda'}, status=status.HTTP_200_OK)

class GetBankAccountsView(APIView):
	"""
	Trae todas las tarjetas de débito
	"""
	def get(self, request, format=None):
		debits = [account.debit for account in BankAccount.objects.all()]
		return Response(debits)
	
