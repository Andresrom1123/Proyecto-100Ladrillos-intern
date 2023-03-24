from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import BankAccount
from core.utils.valid_amount import valid_amount


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
	
# Menu principal
class DepositBankAccountsView(APIView):
	"""
	Hace un nuevo deposito
	"""
	def get_object(self, account_id):
		try:
			return BankAccount.objects.get(id=account_id)
		except BankAccount.DoesNotExist:
			return []
	
	def post(self, request, account_id, format=None):
		try:
			deposit = int(request.data.get('deposit'))
			account = self.get_object(account_id)

			if not deposit:
				return Response({'error': 'Por favor ingresa un déposito'}, status=status.HTTP_400_BAD_REQUEST)
			if not account:
				return Response({'error': 'La tarjeta de débito no existe'}, status=status.HTTP_400_BAD_REQUEST)
			if not valid_amount(deposit):
				return Response({'error': f'{deposit} No es una cantidad válida. Es ilegal falsificar billetes'}, status=status.HTTP_400_BAD_REQUEST)

			account.amount += deposit
			account.save()
			return Response({'success': f'Se ha depositado ${deposit} pesos en su cuenta. Su saldo actual es de {account.amount}'}, status=status.HTTP_200_OK)
		except:
			deposit = request.data.get('deposit')
			return Response({'error': f'"{deposit}" No es una cantidad válida. Por favor vuelve a intentarlo'}, status=status.HTTP_400_BAD_REQUEST)
		

class WithdrawBankAccountsView(APIView):
	"""
	Hace un nuevo retiro
	"""
	def get_object(self, account_id):
		try:
			return BankAccount.objects.get(id=account_id)
		except BankAccount.DoesNotExist:
			return []
	
	def post(self, request, account_id, format=None):
		try:
			withdraw = int(request.data.get('withdraw'))
			account = self.get_object(account_id)

			total_amount = sum([account.amount for account in BankAccount.objects.all()])
			total_withdraw = sum([account.withdraw for account in BankAccount.objects.all()])

			total_amount_with_percentage = total_amount * 0.80
			total_withdraw_with_withdraw = total_withdraw + withdraw

			if not withdraw:
				return Response({'error': 'Por favor ingresa un retiro'}, status=status.HTTP_400_BAD_REQUEST)
			if not account:
				return Response({'error': 'La tarjeta de débito no existe'}, status=status.HTTP_400_BAD_REQUEST)
			if not valid_amount(withdraw):
				return Response({'error': f'{withdraw} No es una cantidad válida. Es ilegal falsificar billetes'}, status=status.HTTP_400_BAD_REQUEST)
			if withdraw > account.amount:
				return Response(
					{'error': f'Su cuenta no tiene ${withdraw} de saldo disponible para retiro. Su saldo actual es de ${account.amount}'}, status=status.HTTP_400_BAD_REQUEST)
			if total_withdraw_with_withdraw > total_amount_with_percentage:
				valid_withdraw = total_amount_with_percentage - total_withdraw
				return Response(
					{'error': f'El cajero no dispone de billetes suficientes para su solicitud, puede solicitar hasta un maximo de ${valid_withdraw} para retirar.'}, status=status.HTTP_400_BAD_REQUEST)


			account.amount -= withdraw
			account.withdraw += withdraw
			account.save()
			return Response({'success': f'Se ha retirado ${withdraw} pesos en su cuenta. Su saldo actual es de {account.amount}'}, status=status.HTTP_200_OK)
		except:
			withdraw = request.data.get('withdraw')
			return Response({'error': f'"{withdraw}" No es una cantidad válida. Por favor vuelve a intentarlo'}, status=status.HTTP_400_BAD_REQUEST)
		

