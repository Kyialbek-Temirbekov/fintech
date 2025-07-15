from django.contrib import admin
from ledger.models import *

admin.site.register(BalanceArticle)
admin.site.register(BalanceGroup)
admin.site.register(Account)
admin.site.register(Transaction)
