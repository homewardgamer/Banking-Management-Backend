from django.urls import path

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
    path("user/delete/<user_id>", user_delete_view),
    path("transaction/new", transaction_add_view),
    path("transaction/view/all", all_transactions_by_customer),
    path("account/create", account_add_view),
]
