from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from apps.trades.api.serializers import TradeSerializer
from apps.common.serializers import InputSerializer
from apps.trades.models import Trade
from services.synchronizer import Synchronizer


class TradesWithCashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        # TODO: Handle creation of only new trades
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        synchronizer = Synchronizer(
            serializer.validated_data['file'],
            columns_to_rename=serializer.validated_data["column_mapping"],
            multiple_sheets=serializer.validated_data[
                "sheet_mapping"] if "sheet_mapping" in serializer.validated_data else None,
            values_to_replace=serializer.validated_data[
                "values_to_replace"] if "values_to_replace" in serializer.validated_data else None,
            merge_columns=serializer.validated_data[
                "merge_columns"] if "merge_columns" in serializer.validated_data else None,
            file_mapping=serializer.validated_data[
                "file_mapping"] if "file_mapping" in serializer.validated_data else None
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


class TradesDetailView(APIView):
    def get(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        serializer = TradeSerializer(trade)

        return Response(serializer.data)

    def put(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        serializer = TradeSerializer(trade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, identifier, *args, **kwargs):
        trade = Trade.objects.get(identifier=identifier)
        trade.delete()
        return Response(f"Trade with identifier: {identifier} has been deleted", status=status.HTTP_204_NO_CONTENT)
