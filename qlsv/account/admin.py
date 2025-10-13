from django.contrib import admin

from .models import (
    Account,
    Tokens
)

# Register your models here
admin.site.register(Account)
admin.site.register(Tokens)
