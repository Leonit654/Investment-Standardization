# sanitization.py

from decimal import Decimal
from cardo.models import Cash_flows, Trade, Operators
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd


class Sanitization:
    @staticmethod
    def get_trade(identifier):
        try:
            # Check if identifier is a float before converting to int
            if isinstance(identifier, float):
                identifier = int(identifier)

            return Trade.objects.get(identifier=identifier)
        except ObjectDoesNotExist:
            # Handle case when the trade doesn't exist
            print(f"Trade with identifier '{identifier}' not found.")
            return None
        except ValueError:
            # Handle case when identifier cannot be converted to int
            print(f"Invalid identifier: '{identifier}'. Unable to convert to int.")
            return None

    @staticmethod
    def clean_and_convert_amount(value):
        if ',' in str(value):
            # Remove commas if they exist
            cleaned_value = value.replace(',', '')
        else:
            cleaned_value = value

        try:
            return Decimal(cleaned_value)
        except ValueError:
            # Handle case when value cannot be converted to Decimal
            print(f"Invalid amount value: '{cleaned_value}'. Unable to convert to Decimal.")
            return None

    @staticmethod
    def get_model_field_type(field_name):
        # Get the field type from the model's meta information
        return Cash_flows._meta.get_field(field_name).__class__

    @staticmethod
    def sanitize_cashflow_data(row, mapping):
        try:
            # Create a copy of the mapping to avoid modifying the original
            current_mapping = mapping.copy()

            trade_identifier_column = current_mapping.get('trade_identifier')
            operation_identifier_column = current_mapping.get('operation')

            trade = Sanitization.get_trade(row[trade_identifier_column])
            amount_column = current_mapping.get('amount')
            amount = Sanitization.clean_and_convert_amount(row[amount_column])

            cashflow_type = row[operation_identifier_column]

            # Handle specific cash flow types or modify as needed
            if cashflow_type == 'cash_order':
                transaction_type = 'withdrawal' if amount < 0 else 'deposit'
            else:
                transaction_type = cashflow_type

            if transaction_type == 'repayment':
                transaction_type = 'general_repayment'

            operation = Operators.objects.get(transaction_type=transaction_type)

            current_mapping.pop('trade_identifier', None)
            current_mapping.pop('cashflow_type', None)

            cashflow_data = {}
            for model_field, excel_column in current_mapping.items():
                cleaned_column = excel_column.replace(" ", "")  # Remove spaces in column names
                model_field_type = Sanitization.get_model_field_type(model_field)

                # Convert data types if needed
                if model_field_type == Decimal:
                    cashflow_data[model_field] = Sanitization.clean_and_convert_amount(row[cleaned_column])
                elif model_field == 'timestamp':
                    # Handle date formatting for 'timestamp'
                    cashflow_data[model_field] = pd.to_datetime(row[cleaned_column], format='%d/%m/%Y').strftime(
                        '%Y-%m-%d')
                else:
                    cashflow_data[model_field] = row[cleaned_column]

            cashflow_data['trade'] = trade
            cashflow_data['amount'] = amount
            cashflow_data['operation'] = operation

            return cashflow_data

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def format_date(date_str, output_format='%Y-%m-%d'):
        """
        Format the date string to the specified output format.

        :param date_str: Input date string
        :param output_format: Desired output format (default is '%Y-%m-%d')
        :return: Formatted date string
        """
        try:
            formatted_date = pd.to_datetime(date_str, format='%d/%m/%Y').strftime(output_format)
            return formatted_date
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return None

    @staticmethod
    def convert_percentage_to_float(percentage_str):
        """
        Convert a percentage string to a float number.

        :param percentage_str: Percentage string (e.g., '10%')
        :return: Float number
        """
        try:
            return float(percentage_str.split('%')[0]) / 100
        except (ValueError, IndexError):
            print(f"Invalid percentage format: {percentage_str}")
            return None
