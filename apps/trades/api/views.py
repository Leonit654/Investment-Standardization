import uuid

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.models import File
from apps.common.serializers import BothInputSerializer
from apps.trades.models import Trade
from services.tasks import synchronizer, logger


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    # def post(self, request, format=None):
    #     # TODO: Handle creation of only new trades
    #     serializer = InputSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     merge_columns = serializer.validated_data.get(
    #         "merge_columns", {}
    #     )
    #     values_to_replace = serializer.validated_data.get("values_to_replace")
    #     synchronizer = Synchronizer(
    #         serializer.validated_data['file'],
    #         file_type="trade",
    #         columns_to_rename=serializer.validated_data["column_mapping"],
    #         merge_columns=merge_columns,
    #         values_to_replace=values_to_replace,
    #     )
    #     try:
    #         synchronizer.run()
    #     except Exception as e:
    #         raise e
    #     return Response("Trades uploaded successfully", status=200)


class TradesWithCashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = BothInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            trades_file = serializer.validated_data['trades_file']
            cashflows_file = serializer.validated_data['cashflows_file']

            column_mapping = serializer.validated_data.get('column_mapping', {})
            values_to_replace = serializer.validated_data.get('values_to_replace', {})
            merge_columns = serializer.validated_data.get('merge_columns', {})

            trade_file_identifier = str(uuid.uuid4()) + serializer.validated_data.get("trades_file").name
            cashflows_file_identifier = str(uuid.uuid4()) + serializer.validated_data.get("cashflows_file").name

            File.objects.create(file_identifier=trade_file_identifier, file=trades_file)
            File.objects.create(file_identifier=cashflows_file_identifier, file=cashflows_file)

            synchronizer.apply_async(
                kwargs={
                    'file_type': "trade",
                    'file_identifier': trade_file_identifier,
                    'columns_to_rename': column_mapping.get('trade'),
                    'merge_columns': merge_columns.get('trade', {}),
                    'values_to_replace': values_to_replace.get('trade'),
                }
            )
            synchronizer.apply_async(
                kwargs={
                    'file_type': "cash_flow",
                    'file_identifier': cashflows_file_identifier,
                    'columns_to_rename': column_mapping.get('cash_flow'),
                    'merge_columns': merge_columns.get('cash_flow', {}),
                    'values_to_replace': values_to_replace.get('cash_flow'),
                }
            )

            return Response("Synchronization started successfully.", status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred during file processing: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
