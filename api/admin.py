from django.contrib import admin
from django.contrib.auth.models import User  # Django's built-in User
from django.contrib.auth.admin import UserAdmin
from .models import ExpenseIncome  # Updated model name

# Unregister the original User admin (optional)
admin.site.unregister(User)

# Register User model with default UserAdmin
admin.site.register(User, UserAdmin)


@admin.register(ExpenseIncome)
class ExpenseIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'transaction_type', 'amount', 'tax', 'tax_type', 'created_at')
    list_filter = ('transaction_type', 'tax_type', 'created_at')
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')
