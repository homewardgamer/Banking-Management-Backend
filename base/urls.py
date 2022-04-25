from django.urls import path

from base.views import *

urlpatterns = [
    path("user/register", UserRegisterView.as_view()),
]
