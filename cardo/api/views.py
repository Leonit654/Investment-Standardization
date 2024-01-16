import pandas as pd
from django.forms import DecimalField
from rest_framework import status
from rest_framework.views import APIView
import datetime as dt
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import render
from cardo.models import Cash_flows, Trade,Operators
from decimal import Decimal
from cardo.api.serializers import TradeSerializer, CashFlowSerializer
from ..forms import MappingForm
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
            df_cashflows['cashflow_date'] = pd.to_datetime(df_cashflows['cashflow_date'],
                                                           format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            # Get the mapping from the request body
            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', '{}'))

            # Map Excel columns to model fields and save to the database
            for index, row in df_cashflows.iterrows():
                try:
                    trade = Trade.objects.get(loan_id=row['loan_id'])
                    cashflow_data = {model_field: row[excel_column] for excel_column, model_field in
                                     cashflow_mapping.items()}
                    cashflow_data['trade'] = trade
                    cashflow = Cash_flows(**cashflow_data)
                    cashflow.save()
                except Trade.DoesNotExist:
                    pass

            return Response("Cash flows uploaded successfully", status=200)

        else:
            return Response("Please upload the trades file", status=400)


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
                    # Convert 'loan_identifier' to int
                    row['loan_identifier'] = int(row['loan_identifier'])

                    # Assuming the user provides a mapping for the loan identifier field
                    loan_identifier_column = cashflow_mapping.get('loan_identifier', 'loan_identifier')
                    operation_identifier_column = cashflow_mapping.get('cashflow_type', 'cashflow_type')

                    # Fetch the Trade object using the loan identifier
                    trade = Trade.objects.get(identifier=row[loan_identifier_column])

                    # Determine the transaction type based on 'cashflow_type' and the sign of 'amount'
                    cashflow_type = row[operation_identifier_column]
                    amount = row['amount']

                    if cashflow_type == 'cash_order':
                        # Check the sign of 'amount' and set the transaction type accordingly
                        if amount < 0:
                            transaction_type = 'withdrawal'
                        else:
                            transaction_type = 'deposit'
                    else:
                        # For other 'cashflow_type', directly use 'cashflow_type' as transaction type
                        transaction_type = cashflow_type

                    # Query the Operators model based on the determined transaction type
                    operation = Operators.objects.get(transaction_type=transaction_type)

                    # Remove loan_identifier_column from the mapping since it's already used to get the Trade
                    cashflow_mapping.pop('loan_identifier', None)

                    # Remove trade_identifier and cashflow_type from the mapping if they exist
                    cashflow_mapping.pop('trade_identifier', None)
                    cashflow_mapping.pop('cashflow_type', None)

                    try:
                        # Continue with the original code
                        cashflow_data = {model_field: row[excel_column] for model_field, excel_column in
                                         cashflow_mapping.items()}
                        cashflow_data['trade'] = trade
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
