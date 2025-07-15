from django import forms

class TransactionForm(forms.Form):
    debit_id = forms.IntegerField()
    credit_id = forms.IntegerField()
    amount = forms.DecimalField(min_value=0.01)
    description = forms.CharField(required=False)
