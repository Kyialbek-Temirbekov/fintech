from django.views.generic import View,ListView
from django.shortcuts import render, redirect

from ledger.forms import TransactionForm
from ledger.services import create_transaction, delete_transaction
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

    def get_queryset(self):
        return Transaction.objects.filter(is_deleted=False)

    def post(self, request):
        transaction_id = request.POST.get('transaction_id')
        if transaction_id:
            delete_transaction(transaction_id)
        return redirect('transaction_list')

