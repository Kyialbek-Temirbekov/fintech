from django.core.exceptions import ValidationError
from django.db import transaction
import logging

from ledger.models import Account, Transaction

def create_transaction(debit_id, credit_id, amount, description):
    try:
        debit_account = Account.objects.get(id=debit_id)
        credit_account = Account.objects.get(id=credit_id)

        if debit_account == credit_account:
            raise ValidationError('Debit and credit accounts must be different')

        with transaction.atomic():
            adjust_balances(debit_account, credit_account, amount)

            debit_account.save()
            credit_account.save()
            Transaction.objects.create(
                debit_account=debit_account,
                credit_account=credit_account,
                amount=amount,
                description=description,
            )
    except ValidationError as e:
        return e.message[0]
    except Exception as e:
        return str(e)
    return 'Transaction created successfully'

def delete_transaction(transaction_id):
    try:
        with transaction.atomic():
            entry = Transaction.objects.get(id=transaction_id)
            adjust_balances(entry.debit_account, entry.credit_account, entry.amount, True)

            entry.debit_account.save()
            entry.credit_account.save()
            entry.is_deleted = True
            entry.save()
            Transaction.objects.create(
                debit_account=entry.credit_account,
                credit_account=entry.debit_account,
                amount=entry.amount,
                description=f'Reverse transaction #{transaction_id}',
            )
    except Exception as e:
        logging.error(e)

def adjust_balances(debit_account, credit_account, amount, reverse=False):
    factor = -1 if reverse else 1
    amount = amount * factor

    if debit_account.type == 'active' and credit_account.type == 'active':
        debit_account.balance += amount
        credit_account.balance -= amount
    elif debit_account.type == 'passive' and credit_account.type == 'passive':
        debit_account.balance -= amount
        credit_account.balance += amount
    elif debit_account.type == 'active' and credit_account.type == 'passive':
        debit_account.balance += amount
        credit_account.balance += amount
    elif debit_account.type == 'passive' and credit_account.type == 'active':
        debit_account.balance -= amount
        credit_account.balance -= amount
    else:
        debit_account.balance += amount
        credit_account.balance -= amount