from rest_framework.test import APITestCase


from bank_accounts.models import BankAccount


class TestBankAccount(APITestCase):
	def setUp(self) -> None:
		self.url_base = 'http://localhost:8000/api/v1/bank/'
		self.account_1 = BankAccount.objects.create(debit='0274764838471045', nip='1923', amount=40)
		self.account_2 = BankAccount.objects.create(debit='3857327576049374', nip='1010', amount=153)


	def test_login_bank_account_view(self):
		url = f'{self.url_base}login/'
		data = {
			'debit': '0274764838471045',
			'nip': '1923'
		}
		response = self.client.post(url, data=data)
		self.assertEqual(response.status_code, 200)

	def test_deposit_bank_account_view(self):
		url = f'{self.url_base}deposit/{self.account_1.debit}/'
		data = {
		 'deposit': 21
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

	def test_withdraw_bank_account_view(self):
		url = f'{self.url_base}withdraw/{self.account_2.debit}/'
		data = {
		 'withdraw': 58
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)

	def test_balance_bank_account_view(self):
		url = f'{self.url_base}balance/{self.account_2.debit}/'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_transfer_bank_account_view(self):
		url = f'{self.url_base}transfer/{self.account_1.debit}/'
		data = {
		 'debit': '3857327576049374',
		 'amount': 12.33
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)