from django import forms
from StripeApp import models


class CurrencyAdminForm(forms.ModelForm):
    class Meta:
        model = models.Currency
        exclude = ['public_api_code']
