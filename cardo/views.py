# sync_app/views.py
from django.shortcuts import render, redirect
from .forms import ColumnMappingForm, RawDataUploadForm
import pandas as pd
from io import BytesIO
import base64

# sync_app/views.py
from django.shortcuts import render, redirect
from .forms import ColumnMappingForm, RawDataUploadForm
import pandas as pd
from io import BytesIO
import base64

def map_columns(request):
    # Simulated list of standard columns (replace with actual field names)
    standard_columns = ['identifier', 'issue_date', 'maturity_date', 'amount', 'invested_amount']

    if request.method == 'POST':
        form = ColumnMappingForm(request.POST, raw_columns=standard_columns)
        if form.is_valid():
            data_mapping = form.cleaned_data['data_mapping']
            data_type = form.cleaned_data['data_type']

            # Save the mapping to the database or perform necessary actions
            # You can store this mapping in a session or a database table

            return redirect('map_columns')  # Redirect to the same page after saving
    else:
        form = ColumnMappingForm(raw_columns=standard_columns)

    return render(request, 'map_columns.html', {'form': form})

def upload_raw_data(request):
    if request.method == 'POST':
        form = RawDataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            raw_data_file = request.FILES['raw_data_file']
            handle_uploaded_raw_data(raw_data_file)
            return redirect('map_columns')  # Redirect to column mapping after uploading raw data
    else:
        form = RawDataUploadForm()

    return render(request, 'upload_raw_data.html', {'form': form})

def handle_uploaded_raw_data(raw_data_file):
    # Save the uploaded file to a specific location or database
    # For simplicity, let's save it to the same directory with the name 'raw_data.xlsx'
    with open('raw_data.xlsx', 'wb') as destination:
        for chunk in raw_data_file.chunks():
            destination.write(chunk)

def download_raw_data(request):
    # Implement logic to download raw data (from the saved raw_data.xlsx file)
    pass

def download_standardized_data(request):
    # Implement logic to download standardized data
    pass
