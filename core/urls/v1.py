from django.urls import path, include
from rest_framework import routers

from bank_accounts import views

urlpatterns = [	
	path('debits/', views.GetBankAccountsView.as_view()),
	path('login/', views.LoginBankAccountsView.as_view()),
	path('deposit/<slug:account_debit>/', views.DepositBankAccountsView.as_view()),
	path('withdraw/<slug:account_debit>/', views.WithdrawBankAccountsView.as_view()),
	path('balance/<slug:account_debit>/', views.BalanceBankAccountsView.as_view()),
	path('transfer/<slug:account_debit>/', views.TransferBankAccountsView.as_view()),
]