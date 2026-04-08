from decimal import Decimal

from django.core.management.base import BaseCommand

from wallet.models import Customer, Transaction


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para demostrar el proyecto Alke Wallet.'

    def handle(self, *args, **options):
        Transaction.objects.all().delete()
        Customer.objects.all().delete()

        customers = [
            {
                'first_name': 'Camila',
                'last_name': 'Rojas',
                'email': 'camila@alke.cl',
                'phone': '+56911111111',
                'transactions': [
                    (Transaction.DEPOSIT, Decimal('500000.00'), 'Abono inicial'),
                    (Transaction.TRANSFER, Decimal('120000.00'), 'Transferencia a proveedor'),
                ],
            },
            {
                'first_name': 'Diego',
                'last_name': 'Mora',
                'email': 'diego@alke.cl',
                'phone': '+56922222222',
                'transactions': [
                    (Transaction.DEPOSIT, Decimal('350000.00'), 'Pago recibido'),
                    (Transaction.WITHDRAWAL, Decimal('50000.00'), 'Retiro en caja'),
                ],
            },
            {
                'first_name': 'Fernanda',
                'last_name': 'Silva',
                'email': 'fernanda@alke.cl',
                'phone': '+56933333333',
                'transactions': [
                    (Transaction.DEPOSIT, Decimal('800000.00'), 'Deposito empresarial'),
                    (Transaction.TRANSFER, Decimal('175000.00'), 'Transferencia programada'),
                    (Transaction.DEPOSIT, Decimal('90000.00'), 'Reembolso'),
                ],
            },
        ]

        for entry in customers:
            customer = Customer.objects.create(
                first_name=entry['first_name'],
                last_name=entry['last_name'],
                email=entry['email'],
                phone=entry['phone'],
            )
            for transaction_type, amount, description in entry['transactions']:
                Transaction.objects.create(
                    customer=customer,
                    transaction_type=transaction_type,
                    amount=amount,
                    description=description,
                )

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados correctamente.'))
