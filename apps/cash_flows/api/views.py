import uuid

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cash_flows.models import CashFlow
from apps.common.models import File
from apps.trades.models import Trade
from services.tasks import synchronizer
from apps.common.serializers import InputSerializer
from services.synchronizer import Synchronizer


class CashFlowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        values_to_replace = serializer.validated_data.get(
            "values_to_replace", {}
        )
        merge_columns = serializer.validated_data.get(
            "merge_columns", {}
        )
        column_mapping = serializer.validated_data["column_mapping"]

        file = serializer.validated_data.get("file")
        file_identifier = str(uuid.uuid4()) + serializer.validated_data.get("file").name


        File.objects.create(file_identifier=file_identifier, file=file)
        try:
            synchronizer.apply_async(
                kwargs={
                    'file_type': "cash_flow",
                    'file_identifier': file_identifier,
                    'columns_to_rename': column_mapping,
                    'merge_columns': merge_columns,
                    'values_to_replace': values_to_replace,
                }
            )

            return Response("CashFlow synchronization started successfully.", status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Cash flows uploaded successfully", status=200)
