from django.shortcuts import render
from .forms import RawDataForm
from django import forms
import pandas as pd

STANDARD_COLUMNS = [
    ('', 'Select a column'),
    ('identifier', 'Identifier'),
    ('issue_date', 'Issue Date'),
    ('maturity_date', 'Maturity Date'),
    ('invested_amount', 'Invested Amount'),
    ('debtor_identifier', 'Debtor Identifier'),
    ('seller_identifier', 'Seller Identifier'),
]


def upload_file(request):
    if request.method == 'POST':
        form = RawDataForm(request.POST, request.FILES)

        if form.is_valid():
            raw_data_file = request.FILES['raw_data_file']

            if raw_data_file.name.endswith('.xlsx'):
                raw_data_df = pd.read_excel(raw_data_file)
            else:
                raw_data_df = pd.read_csv(raw_data_file)

            column_names = list(raw_data_df.columns)

            for field_name, field in form.fields.items():
                if isinstance(field, forms.ChoiceField):
                    form.fields[field_name].choices = [(col, col) for col in column_names]

            form = RawDataForm(request.POST, request.FILES)
            print(column_names)
            return render(request, 'result.html', {'column_names': column_names, 'form': form})
    else:
        form = RawDataForm()

    return render(request, 'upload.html', {'form': form})

