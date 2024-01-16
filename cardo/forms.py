# forms.py
from django import forms

class MappingForm(forms.Form):
    file = forms.FileField(label='Upload File')
    identifier = forms.ChoiceField(label='Identifier Column', choices=[])
    issue_date = forms.ChoiceField(label='Issue Date Column', choices=[])
    maturity_date = forms.ChoiceField(label='Maturity Date Column', choices=[])
    invested_amount = forms.ChoiceField(label='Invested Amount Column', choices=[])
    debitor_identifier = forms.ChoiceField(label='Debtor Identifier Column', choices=[])
    seller_identifier = forms.ChoiceField(label='Seller Identifier Column', choices=[])



