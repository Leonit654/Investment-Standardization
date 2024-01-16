# forms.py
from django import forms

class RawDataForm(forms.Form):
    raw_data_file = forms.FileField()
    mappings = forms.CharField(max_length=100)
    identifier = forms.ChoiceField(choices=[], required=False)
    issue_date = forms.ChoiceField(choices=[], required=False)
    maturity_date = forms.ChoiceField(choices=[], required=False)
    invested_amount = forms.ChoiceField(choices=[], required=False)
    debtor_identifier = forms.ChoiceField(choices=[], required=False)
    seller_identifier = forms.ChoiceField(choices=[], required=False)
