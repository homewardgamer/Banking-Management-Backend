from django.urls import path

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
    path("user/delete/<user_id>", user_delete_view),
    path("transaction/new", transaction_add_view),
    path("account/create", account_add_view),
]
