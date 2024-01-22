# utils.py

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from cardo.models import Trade, Cash_flows
from django.db.models import DecimalField

class Sanitization:



    @staticmethod
    def clean_and_convert_fields(row, mapping):
        cleaned_data = {}

        for model_field, excel_column in mapping.items():
            cleaned_column = excel_column.replace(" ", "")
            model_field_type = Sanitization.get_model_field_type(model_field)

            if model_field_type == DecimalField:
                cleaned_data[model_field] = Sanitization.clean_and_convert_amount(row[cleaned_column])
            else:
                cleaned_data[model_field] = row[cleaned_column]

        return cleaned_data

    @staticmethod
    def convert_to_proper_date(date_series):
        try:
            return pd.to_datetime(date_series, format='%d/%m/%Y').strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Invalid date format: {e}")
            return None

        return cleaned_data
    @staticmethod
    def clean_and_convert_amount(value):
        if ',' in str(value):
            cleaned_value = value.replace(',', '')
        else:
            cleaned_value = value
        try:
            return float(cleaned_value)
        except ValueError:
            print(f"Invalid amount value: '{cleaned_value}'. Unable to convert to float.")
            return None

    @staticmethod
    def get_trade(identifier):
        try:
            if isinstance(identifier, float):
                identifier = int(identifier)
            return Trade.objects.get(identifier=identifier)
        except ObjectDoesNotExist:
            print(f"Trade with identifier '{identifier}' not found.")
            return None
        except ValueError:
            print(f"Invalid identifier: '{identifier}'. Unable to convert to int.")
            return None

    @staticmethod
    def get_model_field_type(field_name):
        return Cash_flows._meta.get_field(field_name).__class__



