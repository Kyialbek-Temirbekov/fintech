from django.views.generic import ListView

from ledger.models import Account


class AccountListView(ListView):
    model = Account
    template_name = 'ledger/account_list.html'
    context_object_name = 'accounts'
