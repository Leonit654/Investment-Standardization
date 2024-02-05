import uuid
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializers import BothInputSerializer
from services.tasks import synchronizer, logger


class Trade_Cashflow(APIView):
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
                    'merge_columns': merge_columns.get('trade',{}),
                    'values_to_replace': values_to_replace.get('trade'),
                }
            )
            synchronizer.apply_async(
                kwargs={
                    'file_type': "cash_flow",
                    'file_identifier': cashflows_file_identifier,
                    'columns_to_rename': column_mapping.get('cash_flow'),
                    'merge_columns': merge_columns.get('cash_flow',{}),
                    'values_to_replace': values_to_replace.get('cash_flow'),
                }
            )

            return Response("Synchronization started successfully.", status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred during file processing: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
