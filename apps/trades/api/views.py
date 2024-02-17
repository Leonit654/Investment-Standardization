import uuid

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.models import File
from apps.trades.api.serializers import TradeSerializer
from apps.common.serializers import InputSerializer
from apps.trades.models import Trade
from services.synchronizer import Synchronizer
from services.tasks import synchronizer


class TradesWithCashflowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        file = serializer.validated_data.get('file')
        column_mapping = serializer.validated_data.get('column_mapping', {})
        values_to_replace = serializer.validated_data.get('values_to_replace', {})
        merge_columns = serializer.validated_data.get('merge_columns', {})
        sheet_mapping = serializer.validated_data.get('sheet_mapping', {})
        file_mapping = serializer.validated_data.get('file_mapping', {})
        task_ids = []
        for file in file:
            file_identifier = str(uuid.uuid4()) + file.name
            file = File.objects.create(file_identifier=file_identifier,
                                       file=file, file_name=list(file_mapping.keys())[0] if file_mapping.keys() else file.name)

            task = synchronizer.apply_async(
                kwargs={
                    'file_identifier': file_identifier,
                    'columns_to_rename': column_mapping,
                    'merge_columns': merge_columns,
                    'values_to_replace': values_to_replace,
                    'sheet_mapping': sheet_mapping,
                    'file_mapping': file_mapping,
                    'file_name': file.file_name
                }
            )
            task_ids.append(task.id)
        return Response({"task_ids": task_ids, "message": "Synchronization started successfully."},
                        status=status.HTTP_202_ACCEPTED)


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
