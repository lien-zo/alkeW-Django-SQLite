from django.contrib import admin

from .models import Customer, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email', 'phone', 'balance')
	search_fields = ('first_name', 'last_name', 'email')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('customer', 'transaction_type', 'amount', 'created_at')
	list_filter = ('transaction_type', 'created_at')
	search_fields = ('customer__first_name', 'customer__last_name', 'description')
