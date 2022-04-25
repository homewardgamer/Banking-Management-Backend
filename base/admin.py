from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.forms import NewUserCreationForm
from base.models import User


class NewUserAdmin(UserAdmin):
    model = User
    add_form = NewUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        ("Additional", {"fields": ("address", "dob")}),
    )


admin.site.register(User, NewUserAdmin)
