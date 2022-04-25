from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    address = models.CharField(_("address"), max_length=300, blank=True)
    dob = models.DateField(_("dob"), null=True)
    is_customer = models.BooleanField(_("is_customer"), default=False)
    is_employee = models.BooleanField(_("is_employee"), default=False)
