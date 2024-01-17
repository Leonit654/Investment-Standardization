import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import DecimalField
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from cardo.models import Cash_flows, Trade,Operators

import json


class MappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')
        cashflow_file = request.FILES.get('cash_flows')

        if trade_file:
            df_trades = pd.read_excel(trade_file)

            # Get the mapping from the request body
            trade_mapping = json.loads(request.data.get('trade_mapping', '{}'))
            print(trade_mapping)


            # Map Excel columns to model fields and save to the database
            for index, row in df_trades.iterrows():
                # Ensure 'issue_date' is provided in trade_data, if not, set it to None
                trade_data = {model_field: row[excel_column] if pd.notna(row[excel_column]) else None
                              for model_field, excel_column in trade_mapping.items()}
                print(trade_data)
                trade_data['issue_date'] = pd.to_datetime(trade_data['issue_date'],
                                                          format='%d/%m/%Y').strftime('%Y-%m-%d')
                trade_data['maturity_date'] = pd.to_datetime(trade_data['maturity_date'],
                                                             format='%d/%m/%Y').strftime('%Y-%m-%d')

                trade = Trade(**trade_data)
                trade.save()

            return Response("Trades uploaded successfully", status=200)


        elif cashflow_file:

            df_cashflows = pd.read_excel(cashflow_file)

            # Get the mapping from the request body

            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', '{}'))

            # Map Excel columns to model fields and save to the database

            for index, row in df_cashflows.iterrows():

                try:

                    loan_id = row[cashflow_mapping.get('trade_identifier')]
                    print(loan_id)
                    cashflow_type = row[cashflow_mapping.get('operation')]
                    print(cashflow_type)


                    # Fetch the Trade object based on loan_id

                    trade = Trade.objects.get(identifier=loan_id)
                    # print(trade)
                    operation = Operators.objects.get(transaction_type=cashflow_type)
                    # print(operation)


                    cashflow_data = {

                        model_field: row[excel_column] if pd.notna(row[excel_column]) else None

                        for model_field, excel_column in cashflow_mapping.items()

                    }
                    print(cashflow_data)

                    # Include the 'trade' field in cashflow_data

                    cashflow_data['trade_identifier'] = trade
                    cashflow_data['operation'] = operation

                    cashflow_data['timestamp'] = pd.to_datetime(cashflow_data['timestamp'],

                                                                format='%d/%m/%Y').strftime('%Y-%m-%d')

                    cashflow = Cash_flows(**cashflow_data)



                    cashflow.save()

                except Trade.DoesNotExist:

                  return  Response("Error uploading cashflow", status=400)

            return Response("Cash flows uploaded successfully", status=200)

class CashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cash_flows')

        if cashflow_file:
            df_cashflows = pd.read_excel(cashflow_file)
            df_cashflows['cashflow_date'] = pd.to_datetime(df_cashflows['cashflow_date'],
                                                           format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', '{}'))

            for index, row in df_cashflows.iterrows():
                try:
                    # Create a copy of the mapping to avoid modifying the original
                    current_mapping = cashflow_mapping.copy()

                    trade_identifier_column = current_mapping.get('trade_identifier')

                    operation_identifier_column = current_mapping.get('operation')

                    trade = self.get_trade(row[trade_identifier_column])

                    amount_column = current_mapping.get('amount')
                    amount = self.clean_and_convert_amount(row[amount_column])

                    cashflow_type = row[operation_identifier_column]

                    if cashflow_type == 'cash_order':
                        # Check the sign of 'amount' and set the transaction type accordingly
                        transaction_type = 'withdrawal' if amount < 0 else 'deposit'
                    else:
                        transaction_type = cashflow_type

                    if transaction_type == 'repayment':
                        transaction_type = 'general_repayment'
                    operation = Operators.objects.get(transaction_type=transaction_type)

                    current_mapping.pop('trade_identifier', None)
                    current_mapping.pop('cashflow_type', None)

                    try:
                        cashflow_data = {}
                        for model_field, excel_column in current_mapping.items():
                            cleaned_column = excel_column.replace(" ", "")  # Remove spaces in column names
                            model_field_type = self.get_model_field_type(model_field)

                            # Convert data types if needed
                            if model_field_type == DecimalField:
                                cashflow_data[model_field] = self.clean_and_convert_amount(row[cleaned_column])
                            else:
                                cashflow_data[model_field] = row[cleaned_column]

                        cashflow_data['trade'] = trade
                        cashflow_data['amount'] = amount
                        cashflow_data['operation'] = operation

                        cashflow = Cash_flows(**cashflow_data)
                        cashflow.save()

                    except Exception as e:
                        print(f"An error occurred: {e}")

                except Exception as e:
                    print(e)

            return Response("Cash flows uploaded successfully", status=200)

        else:
            return Response("Please upload the cashflows file", status=400)

    def get_trade(self, identifier):
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

    def clean_and_convert_amount(self, value):
        if ',' in str(value):
            # Remove commas if they exist
            cleaned_value = value.replace(',', '')
        else:
            cleaned_value = value


        try:
            return float(cleaned_value)
        except ValueError:
            # Handle case when value cannot be converted to float
            print(f"Invalid amount value: '{cleaned_value}'. Unable to convert to float.")
            return None



    def get_model_field_type(self, field_name):
        # Get the field type from the model's meta information
        return Cash_flows._meta.get_field(field_name).__class__

class GetTradeColumns(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')

        if trade_file:
            df_trades1 = pd.read_excel(trade_file)

            excel_file_columns = df_trades1.columns
            print(excel_file_columns)

            return Response(excel_file_columns, status=status.HTTP_200_OK)
class GetCashflowColumns(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cashflows')

        if cashflow_file:
            df_cashflow = pd.read_excel(cashflow_file)

            excel_file_columns = df_cashflow.columns
            print(excel_file_columns)

            return Response(excel_file_columns, status=status.HTTP_200_OK)


class GetStandardFiled(APIView):
    def get(self, request):
        standard_data = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'debitor_identifier',
                         'seller_identifier']

        return Response(standard_data, status=status.HTTP_200_OK)
