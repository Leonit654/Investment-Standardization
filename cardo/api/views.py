from io import BytesIO
from cardo.api.serializers import CashFlowWithTransactionTypeSerializer, RawDataSerializer
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist

from cardo.serializers import *

from cardo.util import Sanitization

from django.http import HttpResponse, FileResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from cardo.models import Cash_flows, Trade, Operators, RawData

from django.shortcuts import get_object_or_404

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

            trade_mapping = json.loads(request.data.get('trade_mapping', '{}'))

            print(trade_mapping)

            # Map Excel columns to model fields and save to the database

            for index, row in df_trades.iterrows():
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

        if not cashflow_file:
            return Response("Please upload the cashflows file", status=400)

        try:

            df_cashflows = pd.read_excel(cashflow_file)

            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', {}))

            cashflows_to_create = []

            for _, row in df_cashflows.iterrows():
                try:
                    current_mapping = cashflow_mapping.copy()
                    trade_identifier_column = current_mapping.pop('trade_identifier', None)

                    if trade_identifier_column:
                        trade_value = row[trade_identifier_column]
                        if pd.notna(trade_value):
                            trade = Sanitization.get_trade(trade_value)
                        else:
                            continue
                    else:
                        trade = None

                    operation_identifier_column = current_mapping.pop('operation', None)

                    if operation_identifier_column:
                        cashflow_type = row[operation_identifier_column]
                        transaction_type = 'withdrawal' if cashflow_type == 'cash_order' and row[
                            'amount'] < 0 else cashflow_type

                        if transaction_type == 'repayment':
                            transaction_type = 'general_repayment'

                        operation = Operators.objects.get(transaction_type=transaction_type)
                    else:
                        operation = None

                    cashflow_data = Sanitization.clean_and_convert_fields(row, current_mapping)

                    cashflow_data['trade'] = trade
                    cashflow_data['amount'] = Sanitization.clean_and_convert_amount(
                        row['amount']) if 'amount' in row else None
                    cashflow_data['operation'] = operation
                    cashflow_data['timestamp'] = Sanitization.convert_to_proper_date(cashflow_data['timestamp'])

                    cashflows_to_create.append(Cash_flows(**cashflow_data))

                except ObjectDoesNotExist as e:
                    print(f"Trade not found: {e}")
                except ValueError as e:
                    print(f"Invalid value: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

            Cash_flows.objects.bulk_create(cashflows_to_create)
            raw_data = RawData(file=cashflow_file)
            raw_data.save()
            return Response("Cash flows uploaded successfully", status=200)

        except Exception as e:
            print(f"An error occurred while processing the cashflows file: {e}")
            return Response("An error occurred while processing the cashflows file", status=500)


class GetTradeColumns(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')

        if trade_file:
            try:
                df_trades1 = pd.read_excel(trade_file)
                excel_file_columns = df_trades1.columns.tolist()

                return Response(excel_file_columns, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)


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


class RealizedAmountView(APIView):
    def post(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        reference_date = request.data.get('reference_date', '2023-12-04')
        realized_amount = trade.get_realized_amount(reference_date)
        return Response({"realized_amount": realized_amount}, status=status.HTTP_200_OK)


class GrossExpectedAmountView(APIView):
    def post(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        reference_date = request.data.get('reference_date', '2023-12-04')
        gross_expected_amount = trade.get_gross_expected_amount(reference_date)
        return Response({"gross_expected_amount": gross_expected_amount}, status=status.HTTP_200_OK)


class RemainingInvestedAmountView(APIView):
    def post(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        reference_date = request.data.get('reference_date', '2023-12-04')
        remaining_invested_amount = trade.get_remaining_invested_amount(reference_date)
        return Response({"remaining_invested_amount": remaining_invested_amount}, status=status.HTTP_200_OK)


class ClosingDateView(APIView):
    def get(self, request, identifier, *args, **kwargs):
        try:
            # Fix the typo here: change `laon_id` to `loan_id`
            trade = Trade.objects.get(identifier=identifier)
            closing_date = trade.get_closing_date()
            return Response(closing_date, status=status.HTTP_200_OK)
        except Trade.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TradeListView(APIView):
    def get(self, request, *args, **kwargs):
        trades = Trade.objects.all()
        serializer = TradeListSerializer(trades, many=True)
        return Response({"trades": serializer.data}, status=status.HTTP_200_OK)


class TradeDetailView(APIView):
    def get(self, request, identifier, *args, **kwargs):
        try:
            trade = Trade.objects.get(identifier=identifier)
            serializer = TradeDetailSerializer(trade)
            return Response({"trade": serializer.data}, status=status.HTTP_200_OK)
        except Trade.DoesNotExist:
            return Response({"error": "Trade not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
