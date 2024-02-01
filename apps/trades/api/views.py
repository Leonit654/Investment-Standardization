from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.serializers import InputSerializer
from apps.trades.models import Trade
from services.synchronizer import Synchronizer
from apps.cash_flows.models import CashFlow


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        # TODO: Handle creation of only new trades
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        merge_columns = serializer.validated_data.get(
            "merge_columns", {}
        )
        values_to_replace = serializer.validated_data.get("values_to_replace")
        synchronizer = Synchronizer(
            serializer.validated_data['file'],
            file_type="trade",
            columns_to_rename=serializer.validated_data["column_mapping"],
            merge_columns=merge_columns,
            values_to_replace=values_to_replace
        )
        try:
            synchronizer.run()
        except Exception as e:
            raise e
        return Response("Trades uploaded successfully", status=200)


class TradesWithCashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        # TODO: Handle creation of only new trades
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        Trade.objects.all().delete()
        CashFlow.objects.all().delete()
        synchronizer = Synchronizer(
            serializer.validated_data['file'],
            columns_to_rename=serializer.validated_data["column_mapping"],
            multiple_sheets=serializer.validated_data["sheet_mapping"],
            values_to_replace=serializer.validated_data["values_to_replace"],
            merge_columns=serializer.validated_data["merge_columns"]
        )
        try:
            synchronizer.run()
        except Exception as e:
            raise e
        return Response("Trades and chash flows  uploaded successfully", status=200)


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
            trade = Trade.objects.get(identifier=identifier)
            closing_date = trade.get_closing_date()
            return Response(closing_date, status=status.HTTP_200_OK)
        except Trade.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)