from decimal import Decimal

from django.db.models import Count, DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .models import Customer, Transaction


class DashboardView(TemplateView):
	template_name = 'wallet/dashboard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['customer_count'] = Customer.objects.count()
		context['transaction_count'] = Transaction.objects.count()
		context['total_balance'] = Customer.objects.aggregate(
			total=Coalesce(
				Sum('balance'),
				Value(Decimal('0.00')),
				output_field=DecimalField(max_digits=12, decimal_places=2),
			)
		)['total']
		context['recent_transactions'] = Transaction.objects.select_related('customer')[:5]
		context['top_customers'] = Customer.objects.annotate(
			transaction_total=Count('transactions')
		).order_by('-balance', 'first_name')[:5]
		return context


class CustomerListView(ListView):
	model = Customer
	template_name = 'wallet/customer_list.html'
	context_object_name = 'customers'


class CustomerDetailView(DetailView):
	model = Customer
	template_name = 'wallet/customer_detail.html'
	context_object_name = 'customer'


class CustomerCreateView(CreateView):
	model = Customer
	template_name = 'wallet/customer_form.html'
	fields = ['first_name', 'last_name', 'email', 'phone']
	success_url = reverse_lazy('wallet:customer_list')


class CustomerUpdateView(UpdateView):
	model = Customer
	template_name = 'wallet/customer_form.html'
	fields = ['first_name', 'last_name', 'email', 'phone']
	success_url = reverse_lazy('wallet:customer_list')


class CustomerDeleteView(DeleteView):
	model = Customer
	template_name = 'wallet/customer_confirm_delete.html'
	success_url = reverse_lazy('wallet:customer_list')


class TransactionListView(ListView):
	model = Transaction
	template_name = 'wallet/transaction_list.html'
	context_object_name = 'transactions'

	def get_queryset(self):
		return Transaction.objects.select_related('customer')


class TransactionDetailView(DetailView):
	model = Transaction
	template_name = 'wallet/transaction_detail.html'
	context_object_name = 'transaction'


class TransactionCreateView(CreateView):
	model = Transaction
	template_name = 'wallet/transaction_form.html'
	fields = ['customer', 'transaction_type', 'amount', 'description']
	success_url = reverse_lazy('wallet:transaction_list')


class TransactionUpdateView(UpdateView):
	model = Transaction
	template_name = 'wallet/transaction_form.html'
	fields = ['customer', 'transaction_type', 'amount', 'description']
	success_url = reverse_lazy('wallet:transaction_list')


class TransactionDeleteView(DeleteView):
	model = Transaction
	template_name = 'wallet/transaction_confirm_delete.html'
	success_url = reverse_lazy('wallet:transaction_list')
