from django.contrib import admin

from .models import Payment, User

admin.site.register(Payment)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email")
