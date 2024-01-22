import json

import pandas as pd
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.trades.api.serializers import TradeSerializer
from apps.trades.models import Trade
from services.file_reader import FileReader
from services.sanitization import Sanitizer


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        trade_file = request.FILES.get('trades')
        df = FileReader(trade_file).read()
        trade_mapping = json.loads(request.data.get('trade_mapping', '{}'))
        df = df.rename(columns={value: key for key, value in trade_mapping.items()})
        sanitizer = Sanitizer(df, data_type_mapping=Trade.get_field_types(), columns_to_keep=Trade.get_field_names())
        sanitizer.run()
        data = sanitizer.df.to_dict(orient="records")
        trades = [Trade(**row) for row in data]
        Trade.objects.bulk_create(trades)
        return Response("Trades uploaded successfully", status=200)


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
