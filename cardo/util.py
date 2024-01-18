# utils.py

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from cardo.models import Trade, Cash_flows
from django.db.models import DecimalField

class Sanitization:
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



    @staticmethod
    def convert_to_proper_date(date_string, input_format='%d/%m/%Y', output_format='%Y-%m-%d'):
        try:
            return pd.to_datetime(date_string, format=input_format).strftime(output_format)
        except ValueError:
            print(f"Invalid date format: {date_string}")
            return None