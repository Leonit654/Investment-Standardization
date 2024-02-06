
from rest_framework.parsers import MultiPartParser
from services.tasks import synchronizer, logger
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import BothInputSerializer
from .models import File
import uuid

from ..cash_flows.models import CashFlow
from ..trades.models import Trade


class Trade_Cashflow(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = BothInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            trades_file = serializer.validated_data.get('trades_file')
            cashflows_file = serializer.validated_data.get('cashflows_file')

            column_mapping = serializer.validated_data.get('column_mapping', {})
            values_to_replace = serializer.validated_data.get('values_to_replace', {})
            merge_columns = serializer.validated_data.get('merge_columns', {})
            sheet_mapping = serializer.validated_data.get('sheet_mapping', {})


            if trades_file:
                trade_file_identifier = str(uuid.uuid4()) + trades_file.name
                File.objects.create(file_identifier=trade_file_identifier, file=trades_file)

                synchronizer.apply_async(
                    kwargs={
                        'file_type': "trade",
                        'file_identifier': trade_file_identifier,
                        'columns_to_rename': column_mapping.get('trade'),
                        'merge_columns': merge_columns.get('trade', {}),
                        'values_to_replace': values_to_replace.get('trade'),
                        'sheet_mapping': sheet_mapping
                    }
                )

            if cashflows_file:
                cashflows_file_identifier = str(uuid.uuid4()) + cashflows_file.name
                File.objects.create(file_identifier=cashflows_file_identifier, file=cashflows_file)

                synchronizer.apply_async(
                    kwargs={
                        'file_type': "cash_flow",
                        'file_identifier': cashflows_file_identifier,
                        'columns_to_rename': column_mapping.get('cash_flow'),
                        'merge_columns': merge_columns.get('cash_flow', {}),
                        'values_to_replace': values_to_replace.get('cash_flow'),
                    }
                )

            return Response("Synchronization started successfully.", status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"Error occurred during file processing: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)