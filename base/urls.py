from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
    path("user/delete/<user_id>", user_delete_view),
    path("transaction/new", transaction_add_view),
    path("account/create", account_add_view),
    path("user/login", obtain_auth_token),
    path("user/logout", user_logout_view),
]
