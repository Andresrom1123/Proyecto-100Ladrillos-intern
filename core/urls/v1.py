from django.urls import path, include
from rest_framework import routers

from bank_accounts import views

urlpatterns = [	
	path('debits/', views.GetBankAccountsView.as_view()),
	path('login/', views.LoginBankAccountsView.as_view()),
	path('locked/<slug:account_id>/', views.LockedBankAccountsView.as_view()),
	path('deposit/<slug:account_id>/', views.DepositBankAccountsView.as_view()),
	path('withdraw/<slug:account_id>/', views.WithdrawBankAccountsView.as_view()),
]