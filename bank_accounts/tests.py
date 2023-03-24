from rest_framework.test import APITestCase


from bank_accounts.models import BankAccount


class TestBankAccount(APITestCase):
	def setUp(self) -> None:
		self.url_base = 'http://localhost:8000/api/v1/bank/'
		self.account_1 = BankAccount.objects.create(debit='0274764838471045', nip='1923')
		self.account_2 = BankAccount.objects.create(debit='3857327576049374', nip='1010')


	def test_login_bank_account_view(self):
		url = f'{self.url_base}login/'
		data = {
			'debit': '0274764838471045',
			'nip': '1923'
		}
		response = self.client.post(url, data=data)
		print(response.data)
		self.assertEqual(response.status_code, 200)

	def test_locked_bank_account_view(self):
		url = f'{self.url_base}locked/2/'
		
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
