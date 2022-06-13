from django.urls import path
from rest_framework.authtoken import views

from .views import *

app_name = 'api'

urlpatterns = [
    path('address/', Address_APIView.as_view()),
    path('address/<int:pk>/', Address_APIView_Detail.as_view()),
    path('declaration-date/', DeclarationDate_APIView.as_view()),
    path('militant/', Militant_APIView.as_view()),
    path('militant/<int:pk>/', Militant_APIView_Detail.as_view()),
    path('core/', Core_APIView.as_view()),
    path('core/<int:pk>/', Core_APIView_Detail.as_view()),
    path('payment/', Payment_APIView.as_view()),
    path('salary/', PaymentDeclaration_APIView.as_view()),
    path('daclaration-date/', DeclarationDate_APIView.as_view()),
    path('payment-date/', Payment_APIView.as_view()),
    path('debts/', Debts_APIView.as_view()),
    path('debts/<str:pk>/', Debts_APIViews_Detail.as_view()),
    path('user/', User_APIView.as_view()),
    path('user/<int:pk>/', User_APIView_Detail.as_view()),
    path('group/', Group_APIView.as_view()),
    path('group/<int:pk>/', Group_APIViews_Details.as_view()),
    path('token-auth/', views.obtain_auth_token)
]
