from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction


class Customer(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, blank=True)
	balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['first_name', 'last_name']

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Transaction(models.Model):
	DEPOSIT = 'deposit'
	WITHDRAWAL = 'withdrawal'
	TRANSFER = 'transfer'

	TRANSACTION_TYPES = [
		(DEPOSIT, 'Deposito'),
		(WITHDRAWAL, 'Retiro'),
		(TRANSFER, 'Transferencia'),
	]

	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
	transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	description = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.get_transaction_type_display()} - {self.customer}'

	def clean(self):
		if self.amount is None or self.amount <= 0:
			raise ValidationError({'amount': 'El monto debe ser mayor que cero.'})

	def balance_impact(self):
		if self.transaction_type == self.DEPOSIT:
			return self.amount
		return Decimal('0.00') - self.amount

	def save(self, *args, **kwargs):
		self.full_clean()

		with transaction.atomic():
			previous_transaction = None
			previous_customer = None
			current_customer = Customer.objects.select_for_update().get(pk=self.customer_id)

			if self.pk:
				previous_transaction = Transaction.objects.select_related('customer').get(pk=self.pk)
				if previous_transaction.customer_id == self.customer_id:
					previous_customer = current_customer
				else:
					previous_customer = Customer.objects.select_for_update().get(pk=previous_transaction.customer_id)

			if previous_transaction is None:
				updated_balance = current_customer.balance + self.balance_impact()
				if updated_balance < 0:
					raise ValidationError('Saldo insuficiente para completar la operacion.')
				current_customer.balance = updated_balance
				current_customer.save(update_fields=['balance', 'updated_at'])
			elif previous_customer.pk == current_customer.pk:
				updated_balance = current_customer.balance - previous_transaction.balance_impact() + self.balance_impact()
				if updated_balance < 0:
					raise ValidationError('Saldo insuficiente para completar la operacion.')
				current_customer.balance = updated_balance
				current_customer.save(update_fields=['balance', 'updated_at'])
			else:
				previous_balance = previous_customer.balance - previous_transaction.balance_impact()
				current_balance = current_customer.balance + self.balance_impact()
				if previous_balance < 0 or current_balance < 0:
					raise ValidationError('Saldo insuficiente para completar la operacion.')
				previous_customer.balance = previous_balance
				current_customer.balance = current_balance
				previous_customer.save(update_fields=['balance', 'updated_at'])
				current_customer.save(update_fields=['balance', 'updated_at'])

			super().save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		with transaction.atomic():
			customer = Customer.objects.select_for_update().get(pk=self.customer_id)
			updated_balance = customer.balance - self.balance_impact()
			if updated_balance < 0:
				raise ValidationError('La eliminacion dejaria un saldo inconsistente.')
			customer.balance = updated_balance
			customer.save(update_fields=['balance', 'updated_at'])
			return super().delete(*args, **kwargs)
