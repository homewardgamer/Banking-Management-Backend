from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.forms import NewUserCreationForm
from base.models import *


class NewUserAdmin(UserAdmin):
    model = User
    add_form = NewUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Additional",
            {"fields": ("address", "dob", "is_customer", "is_employee", "branch")},
        ),
    )


admin.site.register(User, NewUserAdmin)
admin.site.register(Branch)
admin.site.register(Account)
admin.site.register(Transaction)
