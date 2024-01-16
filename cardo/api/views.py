import pandas as pd
from django.forms import DecimalField
from rest_framework import status
from rest_framework.views import APIView
import datetime as dt
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.shortcuts import render
from cardo.models import Cash_flows, Trade
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



class GetHeadExcelView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cash_flows')
        trade_file = request.FILES.get('trades')

        if cashflow_file:
            df_trades1 = pd.read_excel(cashflow_file)

            excel_file_columns = df_trades1.columns
            print(excel_file_columns)

            return Response(excel_file_columns, status=status.HTTP_200_OK)


class GetStandardFiled(APIView):
    def get(self, request):
        standard_data = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'debitor_identifier',
                         'seller_identifier']

        return Response(standard_data, status=status.HTTP_200_OK)
