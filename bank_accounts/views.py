from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import BankAccount
from core.utils.valid_amount import valid_amount, withdraw_amount


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

		if account.nip_incorrect == 3:
			account.locked = True
			account.save()

		if not account:
			return Response({'error': 'Nùmero de tarjeta desconocido.'}, status=status.HTTP_400_BAD_REQUEST)
		if account.locked:
			return Response({'error': 'La cuenta ha sido bloqueada por favor intenta con otra'}, status=status.HTTP_400_BAD_REQUEST)
		if account.nip != nip:
			account.nip_incorrect += 1
			account.save()
			print(account.nip_incorrect)
			return Response({'error': 'Número secreto es incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
		account.nip_incorrect = 0
		account.save()
		return Response(status=status.HTTP_200_OK)
			
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
	def get_object(self, account_debit):
		try:
			return BankAccount.objects.get(debit=account_debit)
		except BankAccount.DoesNotExist:
			return []
	
	def post(self, request, account_debit, format=None):
		try:
			deposit = int(request.data.get('deposit'))
			account = self.get_object(account_debit)

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
	def get_object(self, account_debit):
		try:
			return BankAccount.objects.get(debit=account_debit)
		except BankAccount.DoesNotExist:
			return []
	
	def post(self, request, account_debit, format=None):
		try:
			withdraw = int(request.data.get('withdraw'))
			account = self.get_object(account_debit)

			total_amount = sum([account.amount for account in BankAccount.objects.all()])

			total_amount_with_percentage = total_amount * 0.80

			if not withdraw:
				return Response({'error': 'Por favor ingresa un retiro'}, status=status.HTTP_400_BAD_REQUEST)
			if not account:
				return Response({'error': 'La tarjeta de débito no existe'}, status=status.HTTP_400_BAD_REQUEST)
			if not valid_amount(withdraw):
				return Response({'error': f'{withdraw} No es una cantidad válida. Es ilegal falsificar billetes'}, status=status.HTTP_400_BAD_REQUEST)
			if withdraw > account.amount:
				return Response(
					{'error': f'Su cuenta no tiene ${withdraw} de saldo disponible para retiro. Su saldo actual es de ${account.amount}'}, status=status.HTTP_400_BAD_REQUEST)
			if withdraw > total_amount_with_percentage:
				return Response(
					{'error': f'El cajero no dispone de billetes suficientes para su solicitud, puede solicitar hasta un maximo de ${round(total_amount_with_percentage, 2)} para retirar.'},
					status=status.HTTP_400_BAD_REQUEST)


			account.amount -= withdraw
			account.save()
			return Response({'success': f'Se han retirado ${withdraw} entregando los siguientes billetes:', 'data': withdraw_amount(withdraw)}, status=status.HTTP_200_OK)
		except:
			withdraw = request.data.get('withdraw')
			return Response({'error': f'"{withdraw}" No es una cantidad válida. Por favor vuelve a intentarlo'}, status=status.HTTP_400_BAD_REQUEST)

class BalanceBankAccountsView(APIView):
	"""
	Mustra el saldo de una tarjeta
	"""
	def get_object(self, account_debit):
		try:
			return BankAccount.objects.get(debit=account_debit)
		except BankAccount.DoesNotExist:
			return []
	
	def get(self, request, account_debit, format=None):
		total_amount = sum([account.amount for account in BankAccount.objects.all()])
		total_amount_with_percentage = total_amount * 0.80


		valid_withdraw = total_amount_with_percentage
		account = self.get_object(account_debit)

		if not account:
			return Response({'error': 'La tarjeta de débito no existe'}, status=status.HTTP_400_BAD_REQUEST)
		if valid_withdraw > account.amount and valid_amount(account.amount):
			return Response({'success': f'Su saldo actual es de ${account.amount} y puede retirar todo si lo desea.'}, status=status.HTTP_200_OK)
		if account.amount == 0:
			return Response({'success': f'Su saldo actual es de ${account.amount}.'}, status=status.HTTP_200_OK)

		valid_amount_numbers = list(range(0, account.amount-(account.amount - int(valid_withdraw)) + 1))[::-1]
		valid_amount_number = 0
		for number in valid_amount_numbers:
			if valid_amount(number):
				valid_amount_number = number
				break
		return Response({'success': f'Su saldo actual es de ${account.amount} y puede retirar hasta ${valid_amount_number}'}, status=status.HTTP_200_OK)

class TransferBankAccountsView(APIView):
	"""
	Hace una nueva transferencia
	"""
	def get_object(self, debit):
		try:
			return BankAccount.objects.get(debit=debit)
		except BankAccount.DoesNotExist:
			return []
	def post(self, request, account_debit, format=None):

		try:
			debit = request.data.get('debit')
			amount = float(request.data.get('amount'))

			account_transfer = self.get_object(debit)
			account = get_object_or_404(BankAccount.objects.all(), debit=account_debit)

			if not account_transfer:
				return Response({'error': 'La cuenta a la que desea transferir no existe en este banco'}, status=status.HTTP_400_BAD_REQUEST)
			if account_transfer.locked:
				return Response({'error': 'La cuenta a la que desea transferir esta bloqueada'}, status=status.HTTP_400_BAD_REQUEST)
			if amount > account.amount:
				return Response({'error': f'No cuenta con saldo suficiente, solo puede transferir hasta ${account.amount}'}, status=status.HTTP_400_BAD_REQUEST)
			if account.debit == debit:
				return Response({'error': 'No te puedes transferir a ti mismo'}, status=status.HTTP_400_BAD_REQUEST)
			if amount == 0:
				return Response({'error': 'No puedes transferir $0 pesos.'}, status=status.HTTP_400_BAD_REQUEST)

			account_transfer.amount += round(amount, 2)
			account.amount -= amount

			account.save()
			account_transfer.save()

			return Response({'success': f'Se ha transferido ${round(amount,2)}. Su saldo actual es de ${account.amount}'}, status=status.HTTP_200_OK)
		except:
			amount = request.data.get('amount')
			return Response({'error': f'"{amount}" No es una cantidad válida. Por favor vuelve a intentarlo'}, status=status.HTTP_400_BAD_REQUEST)
