from django.urls import path, include
from rest_framework import routers

from bank_accounts import views

urlpatterns = [	
	path('debits/', views.GetBankAccountsView.as_view()),
]