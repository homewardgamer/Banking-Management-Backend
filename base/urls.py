from django.urls import path

from base.views import *

urlpatterns = [
    path("user/register", user_register_view),
]