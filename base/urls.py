from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
    path("user/delete/<user_id>", user_delete_view),
    path("transaction/new", transaction_add_view),
    path("transaction/view/all", all_transactions_by_customer),
    path("account/create", account_add_view),
    path("account/view/all", account_list_all),
    path("account/view/<account_id>", account_detail_by_id),
    path("account/disable/<account_id>", disable_account),
    path("account/enable/<account_id>", enable_account),
    path("user/login", obtain_auth_token),
    path("user/logout", user_logout_view),
]
