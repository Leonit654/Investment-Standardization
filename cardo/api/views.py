import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.forms import DecimalField
from rest_framework.parsers import MultiPartParser
from cardo.models import Cash_flows, Trade,Operators
import json
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from cardo.util import Sanitization
class MappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')
        cashflow_file = request.FILES.get('cash_flows')

        if trade_file:
            df_trades = pd.read_excel(trade_file)

            trade_mapping = json.loads(request.data.get('trade_mapping', '{}'))

            for index, row in df_trades.iterrows():
                trade_data = {model_field: row[excel_column] if pd.notna(row[excel_column]) else None
                              for model_field, excel_column in trade_mapping.items()}

                trade_data['issue_date'] = pd.to_datetime(trade_data['issue_date'], format='%d/%m/%Y').strftime('%Y-%m-%d')
                trade_data['maturity_date'] = pd.to_datetime(trade_data['maturity_date'], format='%d/%m/%Y').strftime('%Y-%m-%d')
                trade_data['interest_rate'] = float(trade_data['interest_rate'].split('%')[0]) / 100

                trade = Trade(**trade_data)
                trade.save()

            return Response("Trades uploaded successfully", status=200)

        elif cashflow_file:
            df_cashflows = pd.read_excel(cashflow_file)
            df_cashflows['cashflow_date'] = pd.to_datetime(df_cashflows['cashflow_date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            cashflow_mapping = json.loads(request.data.get('cashflow_mapping', '{}'))

            for index, row in df_cashflows.iterrows():
                try:
                    trade = Trade.objects.get(loan_id=row['loan_id'])
                    cashflow_data = {model_field: row[excel_column] for excel_column, model_field in cashflow_mapping.items()}
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
                            trade = None
                    else:
                        trade = None

                    operation_identifier_column = current_mapping.pop('operation', None)

                    if operation_identifier_column:
                        cashflow_type = row[operation_identifier_column]
                        transaction_type = 'withdrawal' if cashflow_type == 'cash_order' and row['amount'] < 0 else cashflow_type

                        if transaction_type == 'repayment':
                            transaction_type = 'general_repayment'

                        operation = Operators.objects.get(transaction_type=transaction_type)
                    else:
                        operation = None

                    cashflow_data = {}

                    for model_field, excel_column in current_mapping.items():
                        cleaned_column = excel_column.replace(" ", "")
                        model_field_type = Sanitization.get_model_field_type(model_field)

                        if model_field_type == DecimalField:
                            cashflow_data[model_field] = Sanitization.clean_and_convert_amount(row[cleaned_column])
                        else:
                            cashflow_data[model_field] = row[cleaned_column]

                    cashflow_data['trade'] = trade
                    cashflow_data['amount'] = Sanitization.clean_and_convert_amount(row['amount']) if 'amount' in row else None
                    cashflow_data['operation'] = operation
                    cashflow_data['timestamp'] = pd.to_datetime(cashflow_data['timestamp'],
                                                                   format='%d/%m/%Y').strftime('%Y-%m-%d')

                    cashflows_to_create.append(Cash_flows(**cashflow_data))

                except ObjectDoesNotExist as e:
                    print(f"Trade not found: {e}")
                except ValueError as e:
                    print(f"Invalid value: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

            Cash_flows.objects.bulk_create(cashflows_to_create)

            return Response("Cash flows uploaded successfully", status=200)

        except Exception as e:
            print(f"An error occurred while processing the cashflows file: {e}")
            return Response("An error occurred while processing the cashflows file", status=500)

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


class CustomLoanPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# class LoanViewSet(viewsets.ModelViewSet):
#     queryset = Trade.objects.all()
#     serializer_class = LoanSerializer
#     pagination_class = CustomLoanPagination
#
#
#
# class CashFlowViewSet(viewsets.ModelViewSet):
#     queryset = CashFlow.objects.all()
#     serializer_class = CashFlowSerializer
#     pagination_class = CustomLoanPagination


# class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer
#     lookup_field = 'loan_id'  # Specify the field to use for the lookup
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#
# class CashFlowDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CashFlow.objects.all()
#     serializer_class = CashFlowSerializer
#     lookup_field = 'cashflow_id'  # Specify the field to use for the lookup
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#







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





