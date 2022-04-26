from django.urls import path

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
    path("transaction/new", transaction_add_view),
    path("account/new", account_add_view),
]
