from django.urls import path
from .views import create_payment, get_account_statement

urlpatterns = [
    path("create-payment/", create_payment, name="create_payment"),
    path("get-statement/", get_account_statement, name="get_account_statement"),
]