from django.views.generic import View,ListView
from django.shortcuts import render, get_object_or_404, redirect

from ledger.forms import TransactionForm
from ledger.services import create_transaction
from ledger.models import Account, Transaction


class AccountListView(ListView):
    model = Account
    template_name = 'ledger/account_list.html'
    context_object_name = 'accounts'

class CreateTransactionView(View):
    template_name = 'ledger/create_transaction.html'

    def get(self, request):
        accounts = Account.objects.all()
        return render(request, self.template_name, {'accounts': accounts, 'message': None})

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            message = create_transaction(**form.cleaned_data)
        else:
            message = form.errors
        accounts = Account.objects.all()
        return render(request, self.template_name, {'accounts': accounts, 'message': message})

class TransactionListView(ListView):
    model = Transaction
    template_name = 'ledger/transaction_list.html'
    context_object_name = 'transactions'
