from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Customer, Transaction


class TransactionModelTests(TestCase):
	def setUp(self):
		self.customer = Customer.objects.create(
			first_name='Ana',
			last_name='Perez',
			email='ana@example.com',
			phone='123456789',
		)

	def test_deposit_updates_customer_balance(self):
		Transaction.objects.create(
			customer=self.customer,
			transaction_type=Transaction.DEPOSIT,
			amount=Decimal('150.00'),
			description='Abono inicial',
		)

		self.customer.refresh_from_db()
		self.assertEqual(self.customer.balance, Decimal('150.00'))

	def test_withdrawal_without_funds_raises_validation_error(self):
		with self.assertRaises(ValidationError):
			Transaction.objects.create(
				customer=self.customer,
				transaction_type=Transaction.WITHDRAWAL,
				amount=Decimal('50.00'),
				description='Retiro sin saldo',
			)

	def test_updating_transaction_recalculates_balance(self):
		transaction = Transaction.objects.create(
			customer=self.customer,
			transaction_type=Transaction.DEPOSIT,
			amount=Decimal('150.00'),
		)

		transaction.amount = Decimal('90.00')
		transaction.save()

		self.customer.refresh_from_db()
		self.assertEqual(self.customer.balance, Decimal('90.00'))

	def test_deleting_transaction_reverts_balance(self):
		transaction = Transaction.objects.create(
			customer=self.customer,
			transaction_type=Transaction.DEPOSIT,
			amount=Decimal('150.00'),
		)

		transaction.delete()

		self.customer.refresh_from_db()
		self.assertEqual(self.customer.balance, Decimal('0.00'))


class WalletViewsTests(TestCase):
	def test_dashboard_and_customer_crud_flow(self):
		create_response = self.client.post(
			reverse('wallet:customer_create'),
			{
				'first_name': 'Luis',
				'last_name': 'Gomez',
				'email': 'luis@example.com',
				'phone': '987654321',
			},
		)

		self.assertRedirects(create_response, reverse('wallet:customer_list'))
		customer = Customer.objects.get(email='luis@example.com')

		dashboard_response = self.client.get(reverse('wallet:dashboard'))
		detail_response = self.client.get(reverse('wallet:customer_detail', args=[customer.pk]))

		self.assertEqual(dashboard_response.status_code, 200)
		self.assertEqual(detail_response.status_code, 200)

	def test_transaction_crud_flow(self):
		customer = Customer.objects.create(
			first_name='Maria',
			last_name='Lopez',
			email='maria@example.com',
		)

		create_response = self.client.post(
			reverse('wallet:transaction_create'),
			{
				'customer': customer.pk,
				'transaction_type': Transaction.DEPOSIT,
				'amount': '200.00',
				'description': 'Deposito de prueba',
			},
		)

		transaction = Transaction.objects.get(customer=customer)
		update_response = self.client.post(
			reverse('wallet:transaction_update', args=[transaction.pk]),
			{
				'customer': customer.pk,
				'transaction_type': Transaction.DEPOSIT,
				'amount': '250.00',
				'description': 'Deposito actualizado',
			},
		)
		delete_response = self.client.post(reverse('wallet:transaction_delete', args=[transaction.pk]))

		self.assertRedirects(create_response, reverse('wallet:transaction_list'))
		self.assertRedirects(update_response, reverse('wallet:transaction_list'))
		self.assertRedirects(delete_response, reverse('wallet:transaction_list'))
		customer.refresh_from_db()
		self.assertEqual(customer.balance, Decimal('0.00'))
