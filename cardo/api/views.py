from decimal import Decimal
from io import BytesIO
from cardo.api.serializers import CashFlowWithTransactionTypeSerializer, CashFlowSerializer, OperationSerializer, TradeSerializer,RawDataSerializer
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import DecimalField
from django.http import HttpResponse, FileResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from cardo.models import Cash_flows, Trade, Operators, RawData
from ..sanitization import Sanitization
from django.shortcuts import get_object_or_404
import os
import json


class DownloadCashflowMappingData(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all data from the model
        queryset = Cash_flows.objects.all()

        # Create a serializer instance for each object in the queryset
        serializer = CashFlowWithTransactionTypeSerializer(queryset, many=True)

        # Create a DataFrame from the serialized data
        df = pd.DataFrame(serializer.data)
        df.drop(columns=['operation'], inplace=True)
        df.rename(columns={'transaction_type': 'operation'}, inplace=True)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
        excel_buffer.seek(0)

        # Set the response headers to force download
        response = HttpResponse(excel_buffer.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=CashFlows.xlsx'

        # Close the BytesIO buffer
        excel_buffer.close()

        return response


class DownloadTradeMappingData(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all data from the model
        queryset = Trade.objects.all()

        # Create a DataFrame from the model data
        df = pd.DataFrame.from_records(queryset.values())

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
        excel_buffer.seek(0)

        # Set the response headers to force download
        response = HttpResponse(excel_buffer.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Trade.xlsx'

        # Close the BytesIO buffer
        excel_buffer.close()

        return response


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')

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
                trade_data['interest_rate'] = Sanitization.convert_percentage_to_float(trade_data['interest_rate'])
                trade_data['issue_date'] = Sanitization.format_date(trade_data['issue_date'])
                trade_data['maturity_date'] = Sanitization.format_date(trade_data['maturity_date'])

                trade = Trade(**trade_data)
                trade.save()

            return Response("Trades uploaded successfully", status=200)


class CashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cash_flows')

        if cashflow_file:
            df_cashflows = pd.read_excel(cashflow_file)

            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', '{}'))

            for index, row in df_cashflows.iterrows():
                try:
                    cashflow_data = Sanitization.sanitize_cashflow_data(row, cashflow_mapping)

                    if cashflow_data:
                        cashflow = Cash_flows(**cashflow_data)
                        cashflow.save()

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


class GetTradeStandardFiled(APIView):
    def get(self, request):
        standard_data = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'debitor_identifier',
                         'seller_identifier']

        return Response(standard_data, status=status.HTTP_200_OK)


class GetTransactionStandardFiled(APIView):
    def get(self, request):
        standard_data = ['operation', 'timestamp', 'amount', 'trade_identifier', 'platform_transaction_id',
                         ]

        return Response(standard_data, status=status.HTTP_200_OK)


class UploadRawDataView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = RawDataSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(file=request.FILES.get('file'))
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, request):
        file_title = request.GET.get("file_title")
        print(file_title)
        filename = request.GET.get("filename")
        print(filename)

        raw_data = get_object_or_404(RawData, file_title=file_title)
        file_path = raw_data.file.path

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

class InsertCardoOperatorsView(APIView):
    def post(self, request, *args, **kwargs):
        # Data to be inserted
        transaction_types = [
            'funding',
            'deposit',
            'withdrawal',
            'general_repayment',
            'principal_repayment',
            'interest_repayment',
        ]

        # Check if each transaction type already exists in the database
        for transaction_type in transaction_types:
            if not Operators.objects.filter(transaction_type=transaction_type).exists():
                Operators.objects.create(transaction_type=transaction_type)

        return HttpResponse("Data inserted successfully.")
